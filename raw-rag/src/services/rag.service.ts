import { Injectable } from '@nestjs/common';
import { EmbeddingService } from './embedding.service';
import { ConfigService } from '@nestjs/config';

@Injectable()
export class RagService {
  private readonly ollamaUrl: string;
  private readonly model: string = 'llama3.2:1b';

  constructor(
    private readonly embeddingService: EmbeddingService,
    private readonly configService: ConfigService,
  ) {
    this.ollamaUrl = this.configService.get<string>(
      'OLLAMA_URL',
      'http://localhost:11434',
    );
  }

  private async generateResponse(prompt: string): Promise<string> {
    try {
      const response = await fetch(`${this.ollamaUrl}/api/generate`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          model: this.model,
          prompt: prompt,
          stream: false,
        }),
      });

      if (!response.ok) {
        throw new Error(`Ollama API error: ${response.statusText}`);
      }

      const data = await response.json();
      return data.response;
    } catch (error) {
      console.error('Error generating response:', error);
      throw error;
    }
  }

  async getAnswer(question: string): Promise<{
    answer: string;
    sources: Array<{
      content: string;
      metadata: any;
    }>;
  }> {
    try {
      // 1. Search for relevant documents
      const searchResults = await this.embeddingService.search(question, 3);

      if (!searchResults.documents?.[0]?.length) {
        return {
          answer: '죄송합니다. 관련된 정보를 찾을 수 없습니다.',
          sources: [],
        };
      }

      const documents = searchResults.documents[0];
      if (!Array.isArray(documents)) {
        throw new Error('Invalid documents format');
      }

      // 2. Construct the prompt
      const context = documents.join('\n\n');
      const prompt = `Here is information about Italian Brainrot characters:

${context}

Based on the above information, please answer the following question:
${question}

Please use only the provided information to answer. If the information is insufficient, please say so.`;

      // 3. Generate answer with LLM
      const answer = await this.generateResponse(prompt);

      // 4. Return the answer with sources
      return {
        answer,
        sources: documents.map((doc, i) => ({
          content: doc,
          metadata: searchResults.metadatas?.[0]?.[i] || {},
        })),
      };
    } catch (error) {
      console.error('Error in RAG:', error);
      throw error;
    }
  }
}
