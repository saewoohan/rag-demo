import { Injectable, OnModuleInit } from '@nestjs/common';
import { ChromaClient, Collection, QueryResponse } from 'chromadb';
import { ConfigService } from '@nestjs/config';
import { randomUUID } from 'crypto';

type ChromaMetadata = {
  [key: string]: string | number | boolean;
};

export interface DocumentMetadata {
  name?: string;
  category?: string;
  features?: string[];
  origin?: string;
  related_characters?: string[];
  type?: string;
  trend_start?: string;
  primary_platform?: string;
  key_features?: string[];
  [key: string]: string | string[] | undefined;
}

export interface CustomQueryResponse extends Omit<QueryResponse, 'metadatas'> {
  metadatas?: DocumentMetadata[][];
}

@Injectable()
export class EmbeddingService implements OnModuleInit {
  private collection!: Collection;
  private readonly collectionName = 'italian_brainrot';
  private readonly embeddingServerUrl: string;
  private readonly chromaUrl: string;

  constructor(private configService: ConfigService) {
    this.embeddingServerUrl = this.configService.get<string>(
      'EMBEDDING_SERVER_URL',
      'http://localhost:8080',
    );
    this.chromaUrl = this.configService.get<string>(
      'CHROMA_URL',
      'http://localhost:8000',
    );
  }

  async onModuleInit() {
    await this.initialize();
  }

  private serializeMetadata(metadata: DocumentMetadata): ChromaMetadata {
    const serialized: ChromaMetadata = {};
    for (const [key, value] of Object.entries(metadata)) {
      if (Array.isArray(value)) {
        serialized[key] = value.join(',');
      } else if (value !== undefined) {
        serialized[key] = value;
      }
    }
    return serialized;
  }

  private deserializeMetadata(metadata: ChromaMetadata): DocumentMetadata {
    const deserialized: DocumentMetadata = {};
    for (const [key, value] of Object.entries(metadata)) {
      if (typeof value === 'string' && value.includes(',')) {
        deserialized[key] = value.split(',');
      } else if (typeof value === 'string') {
        deserialized[key] = value;
      }
    }
    return deserialized;
  }

  private async initialize() {
    try {
      const chromaClient = new ChromaClient({
        path: this.chromaUrl,
      });

      this.collection = await chromaClient.getOrCreateCollection({
        name: this.collectionName,
        metadata: {
          description: 'Italian Brainrot character database',
        },
      });

      const healthCheck = await fetch(`${this.embeddingServerUrl}/health`);
      if (!healthCheck.ok) {
        throw new Error('Embedding server is not running');
      }

      console.log('Embedding service initialized successfully');
    } catch (error) {
      console.error('Error initializing embedding service:', error);
      throw error;
    }
  }

  async generateEmbedding(text: string): Promise<number[]> {
    try {
      const response = await fetch(`${this.embeddingServerUrl}/embed`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          text: this.preprocessText(text),
        }),
      });

      if (!response.ok) {
        throw new Error(`Embedding server error: ${response.statusText}`);
      }

      const data = await response.json();
      return data.embedding;
    } catch (error) {
      console.error('Error generating embedding:', error);
      throw error;
    }
  }

  private preprocessText(text: string): string {
    return text.trim().replace(/\s+/g, ' ').toLowerCase();
  }

  async addDocument(
    text: string,
    metadata: DocumentMetadata = {},
    id?: string,
  ): Promise<string> {
    try {
      const documentId = id || randomUUID();
      const embedding = await this.generateEmbedding(text);
      const serializedMetadata = this.serializeMetadata(metadata);

      await this.collection.add({
        ids: [documentId],
        embeddings: [embedding],
        metadatas: [serializedMetadata],
        documents: [text],
      });

      return documentId;
    } catch (error) {
      console.error('Error adding document:', error);
      throw error;
    }
  }

  async search(
    query: string,
    limit = 3,
    filters?: DocumentMetadata,
  ): Promise<CustomQueryResponse> {
    try {
      const queryEmbedding = await this.generateEmbedding(query);
      const serializedFilters = filters
        ? this.serializeMetadata(filters)
        : undefined;

      const results = await this.collection.query({
        queryEmbeddings: [queryEmbedding],
        nResults: limit,
        where: serializedFilters,
      });

      const customResults: CustomQueryResponse = {
        ...results,
        metadatas: results.metadatas?.map((metadataArray) =>
          metadataArray.map((metadata) =>
            this.deserializeMetadata(metadata as ChromaMetadata),
          ),
        ),
      };

      return customResults;
    } catch (error) {
      console.error('Error searching documents:', error);
      throw error;
    }
  }

  async addBulkDocuments(
    documents: Array<{
      text: string;
      metadata?: DocumentMetadata;
      id?: string;
    }>,
  ) {
    try {
      const embeddings = await Promise.all(
        documents.map((doc) => this.generateEmbedding(doc.text)),
      );

      await this.collection.add({
        ids: documents.map((doc) => doc.id || randomUUID()),
        embeddings,
        metadatas: documents.map((doc) =>
          this.serializeMetadata(doc.metadata || {}),
        ),
        documents: documents.map((doc) => doc.text),
      });
    } catch (error) {
      console.error('Error adding bulk documents:', error);
      throw error;
    }
  }
}
