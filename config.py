class Config:
    SIZE = 3
    SILENT = True
    GUI = True
    AI_WHITE_ENABLE = True
    AI_BLACK_ENABLE = True
    AI_WHITE_ALGORITHM = 'reinforcement_learning'
    AI_BLACK_ALGORITHM = 'random'
    TRAIN_WHITE = True
    TRAIN_BLACK = False
    LEARNING_RATE = 0.3
    EXPLORATION_CHANCE = 0.2
    MODEL_DIRPATH = 'src/ai/'
    MODEL_FILENAME = 'rl_model'
    MODEL_EXTENSION = 'ttm'