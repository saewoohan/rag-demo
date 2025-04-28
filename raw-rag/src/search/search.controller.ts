import { Controller, Post, Get, Body, Param } from '@nestjs/common';
import {
  EmbeddingService,
  DocumentMetadata,
  CustomQueryResponse,
} from '../services/embedding.service';

export class SearchDto {
  query!: string;
  limit?: number;
  filters?: DocumentMetadata;
}

@Controller('search')
export class SearchController {
  constructor(private readonly embeddingService: EmbeddingService) {}

  @Post()
  async search(@Body() searchDto: SearchDto): Promise<CustomQueryResponse> {
    const { query, limit = 3, filters } = searchDto;
    return this.embeddingService.search(query, limit, filters);
  }

  @Get('categories')
  async getCategories(): Promise<string[]> {
    const results = await this.embeddingService.search('', 100);
    const categories = new Set<string>();

    if (results.metadatas?.[0]) {
      for (const metadata of results.metadatas[0]) {
        if (metadata?.category) {
          categories.add(metadata.category);
        }
      }
    }

    return Array.from(categories);
  }

  @Get(':category')
  async searchByCategory(
    @Param('category') category: string,
  ): Promise<CustomQueryResponse> {
    return this.embeddingService.search('', 100, { category });
  }
}
