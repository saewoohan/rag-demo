import { Controller, Post, Body } from '@nestjs/common';
import { RagService } from '../services/rag.service';

export class QuestionDto {
  question!: string;
}

@Controller('rag')
export class RagController {
  constructor(private readonly ragService: RagService) {}

  @Post('ask')
  async ask(@Body() questionDto: QuestionDto) {
    return this.ragService.getAnswer(questionDto.question);
  }
}
