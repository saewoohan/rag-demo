import { Module } from '@nestjs/common';
import { RagController } from './rag.controller';
import { RagService } from '../services/rag.service';
import { SearchModule } from '../search/search.module';

@Module({
  imports: [SearchModule],
  controllers: [RagController],
  providers: [RagService],
})
export class RagModule {}
