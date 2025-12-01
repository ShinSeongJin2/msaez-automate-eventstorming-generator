from typing import List

from ..models import TextChunkModel

class TextChunker:
    @staticmethod
    def split_into_chunks_by_line(text: str, chunk_size: int, spare_size: int) -> List[TextChunkModel]:
        """
        텍스트를 라인 단위로 청크로 분할하고 시작 라인 번호를 함께 반환
        
        Args:
            text: 분할할 텍스트
            chunk_size: 청크의 최대 크기
            spare_size: 중첩(overlap) 처리를 위한 여유 크기
            
        Returns:
            청크 배열 (텍스트와 시작 라인 번호 포함)
        """
        lines = text.split('\n')
        chunks = []
        current_chunk = ''
        current_start_line = 1
        current_line_count = 0
        
        for i in range(len(lines)):
            line = lines[i]
            line_with_newline = line + '\n' if i < len(lines) - 1 else line
            
            # 청크 사이즈 체크
            if TextChunker._get_utf16_length(current_chunk + line_with_newline) > chunk_size and current_chunk:
                # 현재 청크를 저장
                chunks.append(TextChunkModel(
                    text=current_chunk,
                    start_line=current_start_line
                ))
                
                # 중첩(overlap) 처리: 마지막 몇 줄을 다음 청크 시작에 포함
                overlap_lines = TextChunker._get_last_lines(current_chunk, spare_size)
                overlap_line_count = len(overlap_lines.split('\n')) - 1  # 마지막 빈 줄 제외
                
                current_chunk = overlap_lines + line_with_newline
                current_start_line = current_start_line + current_line_count - overlap_line_count
                current_line_count = overlap_line_count + 1
            else:
                current_chunk += line_with_newline
                if current_line_count == 0:
                    current_start_line = i + 1  # 라인 번호는 1부터 시작
                current_line_count += 1
        
        # 마지막 청크 처리
        if current_chunk.strip():
            chunks.append(TextChunkModel(
                text=current_chunk,
                start_line=current_start_line
            ))
        
        return chunks
    
    @staticmethod
    def _get_last_lines(text: str, target_size: int) -> str:
        """
        지정된 크기만큼의 마지막 라인들을 가져오는 헬퍼 메서드
        
        Args:
            text: 텍스트
            target_size: 목표 크기
            
        Returns:
            마지막 라인들
        """
        lines = text.rstrip().split('\n')  # 마지막에 \n이 있을 경우, \n\n으로 의도치 않은 추가가 발생할 수 있음
        result = ''
        
        for i in range(len(lines) - 1, -1, -1):
            line = lines[i]
            line_with_newline = line + '\n' if i > 0 else line
            if TextChunker._get_utf16_length(result + line_with_newline) > target_size:
                break
            result = line_with_newline + result
        
        return result

    # 단순 문자 길이 계산시에 유니코드 문자 길이 계산에 있어서 Javascript와 동일한 결과가 나오도록 처리
    @staticmethod
    def _get_utf16_length(text: str) -> int:
        return len(text.encode('utf-16-le')) // 2