from python_a2a import A2AServer, agent, run_server, TaskStatus, TaskState
import asyncio

@agent(
    name="Streaming Demo Agent",
    description="Demonstrates streaming capabilities",
    version="1.0.0"
)
class StreamingAgent(A2AServer):
    def handle_task(self, task):
        """Regular synchronous response for non-streaming requests."""
        text = self._get_text_from_task(task)
        task.artifacts = [{
            "parts": [{"type": "text", "text": f"Non-streaming response for: {text}"}]
        }]
        task.status = TaskStatus(state=TaskState.COMPLETED)
        return task
    
    async def stream_response(self, message):
        """Stream a response token by token."""
        words = f"Streaming response for: {message}".split()
        
        for word in words:
            yield {"content": word + " "}
            await asyncio.sleep(0.2)  # Simulate thinking time

    def _get_text_from_task(self, task):
        msg = task.message or {}
        content = msg.get("content", {})
        text = content.get("text", "") if isinstance(content, dict) else str(content)
        return text

# Create and run the agent
if __name__ == "__main__":
    streaming_agent = StreamingAgent(url="http://0.0.0.0:5000")
    run_server(streaming_agent, host="0.0.0.0", port=5000)