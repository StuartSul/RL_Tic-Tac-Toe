class Config:
    SIZE = 3
    SILENT = True
    GUI = False
    AI_WHITE_ENABLE = True
    AI_BLACK_ENABLE = True
    AI_WHITE_ALGORITHM = 'reinforcement_learning'
    AI_BLACK_ALGORITHM = 'reinforcement_learning'
    TRAIN_WHITE = True
    TRAIN_BLACK = True
    TARGET_EPOCH = 100000
    SAVE_INTERVAL = 5000
    LEARNING_RATE = 0.3
    EXPLORATION_CHANCE = 0.1
    MODEL_DIRPATH = 'src/ai/'
    MODEL_FILENAME = 'rl_model'
    MODEL_EXTENSION = 'ttm'