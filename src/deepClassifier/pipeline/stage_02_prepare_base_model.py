
from deepClassifier.config import ConfigurationManager
from deepClassifier.components import PrepareBaseModel
from deepClassifier import logger


STAGE_NAME = 'Prepare Base model Stage'

def main():
    try:
        config = ConfigurationManager()     
        prepare_base_model_config = config.get_prepare_base_model_config()
        prepare_base_model = PrepareBaseModel(config=prepare_base_model_config)
        prepare_base_model.get_base_model() 
        prepare_base_model.update_base_model()   
        # prepare_base_model.save_model()  
    except Exception as e: 
        raise e
    

if __name__== '__main__':
    try: 
        logger.info(f'\n\n X<<<<<<<<<<<<-------------->>>>>>>>>>>X \n>>>>>>>>>>>>>>>> stage: {STAGE_NAME} started <<<<<<<<<<<<<<<<')
        main() 
        logger.info(f'>>>>>>>>>>>>>>>> stage: {STAGE_NAME} completed <<<<<<<<<<<<<<<<\n\n X<<<<<<<<<<<<------------------>>>>>>>>>>>X')
    except Exception as e: 
        logger.exception(e)
        raise e
