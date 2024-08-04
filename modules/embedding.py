import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from typing import Generator, List
from http import HTTPStatus
from .config import Config
import dashscope

class EmbeddingModel:
    def __init__(self):
        self.batch_size = Config.DASHSCOPE_MAX_BATCH_SIZE

    def batched(self, inputs: List) -> Generator[List, None, None]:
        for i in range(0, len(inputs), self.batch_size):
            yield inputs[i:i + self.batch_size]

    def embed_with_list_of_str(self, inputs: List):
        result = None  # merge the results.
        batch_counter = 0
        for batch in self.batched(inputs):
            resp = dashscope.TextEmbedding.call(
                model=dashscope.TextEmbedding.Models.text_embedding_v2,
                api_key=Config.QWEN_API,
                input=batch)
            if resp.status_code == HTTPStatus.OK:
                if result is None:
                    result = resp
                else:
                    for emb in resp.output['embeddings']:
                        emb['text_index'] += batch_counter
                        result.output['embeddings'].append(emb)
                    result.usage['total_tokens'] += resp.usage['total_tokens']
            else:
                print(resp)
            batch_counter += len(batch)
        return result


if __name__ == '__main__':
    inputs = ['风急天高猿啸哀', '渚清沙白鸟飞回', '无边落木萧萧下', '不尽长江滚滚来']
    model = EmbeddingModel()
    print(model.embed_with_list_of_str(inputs)["output"]["embeddings"])
