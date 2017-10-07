from keras.models import Sequential
from keras.layers import Dense, Activation, Dropout, TimeDistributed
from keras.layers import GRU, LSTM, Conv2D, Conv1D, Reshape, Flatten, Permute, AveragePooling2D, MaxPooling2D
import keras.optimizers as optimizers

from custom_objects import CustomObjects

class ModelDef(object):

  layers=[]

  model = None
  utils = None
  started = False


  stateful = False


  def __init__(self, utils, config):
    self.utils = utils
    self.config = config

    self.layers=[]


  def define_model(self, frame_seq_len, framelen, num_frame_seqs):
    self.utils.log("Defining model")
    model =  Sequential()
    self.model = model

    self.utils.log("Stateful:", self.stateful)

    time_distributed = False

#    self.add_layer(
#      TimeDistributed(
#        Dense(
#          framelen * 50
#          , activation="relu"
#        )
#        , batch_input_shape=(1 , frame_seq_len, framelen)
#      )
#    )

    if self.stateful:
        self.add_layer(
          LSTM(
            5
            , batch_input_shape=(num_frame_seqs , frame_seq_len, framelen)
            , return_sequences=True
            , trainable=True
            , stateful=self.stateful
        #    ,dropout = 0.1
          )
        )
    else:
        self.add_layer(
          LSTM(
            5
            , input_shape=(frame_seq_len, framelen)
            , return_sequences=True
            , trainable=True
            , stateful=self.stateful
        #    ,dropout = 0.1
          )
        )



    self.add_layer(
      LSTM(
        50
        , return_sequences=True
        , trainable=True
        , stateful=self.stateful
    #    ,dropout = 0.1

      )
    )



    self.add_layer(
      LSTM(
        20
        , return_sequences=True
        , trainable=True
        , stateful=self.stateful
    #    ,dropout = 0.1

      )
    )


    self.add_layer(
      LSTM(
        200
        , return_sequences=True
        , trainable=True
        , stateful=self.stateful
    #    ,dropout = 0.1

      )
    )



    self.add_layer(
      TimeDistributed(
        Dense(
          framelen * 50
          , activation="relu"
        )
        , batch_input_shape=(1 , frame_seq_len, framelen)
      )
    )

    self.add_layer(
      LSTM(
        5
        , return_sequences=True
        , trainable=True
        , stateful=self.stateful
    #    ,dropout = 0.1

      )
    )


    self.add_layer(
      TimeDistributed(
        Dense(
          framelen * 50
          , activation="relu"
        )
        , batch_input_shape=(1 , frame_seq_len, framelen)
      )
    )

    self.add_layer(
      LSTM(
        160
        , input_shape=(frame_seq_len, framelen)
        , return_sequences= time_distributed
        , trainable=True
        , stateful=self.stateful
    #    ,dropout = 0.1
      )
    )


    if time_distributed:
      self.add_layer(
        TimeDistributed(
          Dense(
            framelen
            ,activation="relu"
          )
        )
      )
    else:
      self.add_layer(
        Dense(
          framelen
          ,activation="relu"
        )
      )

    #model.add(Dropout(0.1))

    return model

  # we wrap the model.add method, since in the future we may wish to
  # provide additional processing at this level
  def add_layer(self, layer):
    self.model.add(layer)
    return layer


  # start training GRU 1, then 1&2, then 3
  def before_iteration(self, iteration):
#    if iteration == 541:
#      self.utils.log("Adding frame rotation to reduce memory usage")
#      self.config.limit_frames = self.config.num_frames / 100
#      self.model_updates_lstm_1234_trainable()
#      self.config.log_attrs()


    if not self.started:
      self.model_updates_onstart()

#
#    elif iteration == 481:
#      self.model_updates_lstm3_trainable()
#

    self.started = True

  def model_updates_onstart(self):
#    self.utils.log("Make all lstms trainable")
#    self.model.layers[0].trainable=True
#    self.model.layers[1].trainable=True
#    self.model.layers[2].trainable=True
#    self.model.layers[3].trainable=True
#    self.model.layers[4].trainable=True

    self.compile_model()
    self.utils.save_json_model(0)


  def model_updates_lstm_1234_trainable(self):
    self.utils.log("Make lstm 1,2,3,4 trainable")
    self.model.layers[0].trainable=True
    self.model.layers[1].trainable=True
    self.model.layers[2].trainable=True
    self.model.layers[3].trainable=True
    self.compile_model()
    self.utils.save_json_model(4)

  def model_updates_lstm_123_untrainable(self):
    self.utils.log("Make lstm 1,2,3 untrainable ")
    self.model.layers[0].trainable=False
    self.model.layers[1].trainable=False
    self.model.layers[2].trainable=False
    self.compile_model()
    self.utils.save_json_model(5)

  def model_updates_lstm_123_trainable(self):
    self.utils.log("Make lstm 1,2,3 trainable")
    self.model.layers[0].trainable=True
    self.model.layers[1].trainable=True
    self.model.layers[2].trainable=True
    self.compile_model()
    self.utils.save_json_model(4)

  def model_updates_lstm_23_trainable(self):
    self.utils.log("Make lstm 2,3 trainable")
    self.model.layers[0].trainable=False
    self.model.layers[1].trainable=True
    self.model.layers[2].trainable=True
    self.compile_model()
    self.utils.save_json_model(4)


  def model_updates_lstm2_trainable(self):
    self.utils.log("Make lstm 2 trainable")
    self.model.layers[0].trainable=False
    self.model.layers[1].trainable=True
    self.model.layers[2].trainable=False
    self.compile_model()
    self.utils.save_json_model(1)

  def model_updates_lstm3_trainable(self):
    self.utils.log("Make lstm 3 trainable")
    self.model.layers[0].trainable=False
    self.model.layers[1].trainable=False
    self.model.layers[2].trainable=True
    self.compile_model()
    self.utils.save_json_model(2)

  def model_updates_lstm1_trainable(self):
    self.utils.log("Make lstm 1 trainable")
    self.model.layers[0].trainable=True
    self.model.layers[1].trainable=False
    self.model.layers[2].trainable=False
    self.compile_model()
    self.utils.save_json_model(3)

  def model_updates_lstm12_trainable(self):
    self.utils.log("Make lstm 1 & 2 trainable")
    self.model.layers[0].trainable=True
    self.model.layers[1].trainable=True
    self.model.layers[2].trainable=False
    self.compile_model()
    self.utils.save_json_model(3)


  def load_weights(self, fn, by_name=False):
    self.utils.log("Loading weights")
    self.model.load_weights(fn, by_name=by_name)

  def compile_model(self):
    self.utils.log("Compiling model")

    optimizer_name = self.config.optimizer["name"]
    args = []
    optimizer = getattr(optimizers, optimizer_name)(*args, **self.config.optimizer["params"])
      #optimizer = Nadam() #SGD() #Adam() #RMSprop(lr=0.01)


    #loss = CustomObjects.codec2_param_mean_square_error
    loss = CustomObjects.codec2_param_error
    #loss = 'mean_absolute_error'
    #loss = 'cosine_proximity'
    self.model.compile(loss=loss, optimizer=optimizer)
    self.utils.log_model_summary()
