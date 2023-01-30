from logic.processor.processor import Processor
from connector.mongo_helper import MongoHelper
class Pipeline():
    # processors : [Processor]
    mongo_helper: MongoHelper
    
    def before_process(self, **kwargs):
        pass

    def run(self):
        self.before_process()
        pass
