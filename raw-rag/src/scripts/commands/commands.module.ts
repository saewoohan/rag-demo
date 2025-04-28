import { Module } from '@nestjs/common';
import { LoadDataCommand } from './load-data.command';
import { EmbeddingService } from '../../services/embedding.service';

@Module({
  providers: [LoadDataCommand, EmbeddingService],
})
export class CommandsModule {}
