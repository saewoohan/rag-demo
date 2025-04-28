import { Command, CommandRunner } from 'nest-commander';
import { Injectable } from '@nestjs/common';
import * as fs from 'node:fs';
import * as path from 'node:path';
import { EmbeddingService } from '../../services/embedding.service';

interface Character {
  name: string;
  description: string;
  features: string[];
  category: string;
  origin?: string;
  related_characters?: string[];
}

interface CharacterData {
  characters: Character[];
  metadata: {
    trend_start: string;
    primary_platform: string;
    description: string;
    key_features: string[];
  };
}

@Injectable()
@Command({
  name: 'load:data',
  description: 'Load character data into ChromaDB',
})
export class LoadDataCommand extends CommandRunner {
  constructor(private readonly embeddingService: EmbeddingService) {
    super();
  }

  async run(): Promise<void> {
    try {
      const charactersData: CharacterData = JSON.parse(
        fs.readFileSync(
          path.join(__dirname, '../../data/characters.json'),
          'utf-8',
        ),
      );

      const documents = charactersData.characters.map((character) => ({
        text: `${character.name}: ${character.description} Features: ${character.features.join(
          ', ',
        )}. Category: ${character.category}`,
        metadata: {
          name: character.name,
          category: character.category,
          features: character.features,
          origin: character.origin || 'Unknown',
          related_characters: character.related_characters || [],
        },
      }));

      documents.push({
        text: charactersData.metadata.description,
        metadata: {
          name: 'metadata',
          category: 'metadata',
          features: charactersData.metadata.key_features,
          origin: 'System',
          related_characters: [],
        },
      });

      await this.embeddingService.addBulkDocuments(documents);

      console.log('Successfully loaded all character data into ChromaDB');
    } catch (error) {
      console.error('Error loading data:', error);
      process.exit(1);
    }
  }
}
