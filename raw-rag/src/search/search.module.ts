import { Module } from '@nestjs/common';
import { SearchController } from './search.controller';
import { EmbeddingService } from '../services/embedding.service';

@Module({
  controllers: [SearchController],
  providers: [EmbeddingService],
  exports: [EmbeddingService],
})
export class SearchModule {}
