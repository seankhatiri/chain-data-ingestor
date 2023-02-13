
from logic.pipeline.dynamic_pipeline.dynamic_pipeline import DynamicPipeline


if __name__ == '__main__':
    print('execution started')
    txs = ['transaction1', 'transaction2', 'transaction3']
    processors = ['processor1', 'processor2', 'processor3'] 
    DynamicPipeline(processors, txs)