from eventstorming_generator.terminal.terminal_tests.mocks import text_chunker_expected_chunks
from eventstorming_generator.terminal.commons.util import execute_text_chunker_util

class TestTextChunker:
    """TextChunker 클래스의 테스트"""
    def test_chunk_by_requirements(self):
        """requirements를 청크로 분할하고 올바른 구조를 가지고 있는지 테스트"""
        chunks = execute_text_chunker_util("it_system_requirements")
        assert len(chunks) == 2

        for i, chunk in enumerate(chunks):
            expected_chunk = text_chunker_expected_chunks[i]
            assert chunk.text == expected_chunk.text
            assert chunk.start_line == expected_chunk.start_line