import os
from absl import logging
from pipeline import configs
from pipeline import run_pipeline
from tfx.v1 import orchestration

# TFX pipeline produces many output files and metadata. All output data will be
# stored under this OUTPUT_DIR.
# NOTE: It is recommended to have a separated OUTPUT_DIR which is *outside* of
#       the source code structure. Please change OUTPUT_DIR to other location
#       where we can store outputs of the pipeline.
OUTPUT_DIR = '.'

# TFX produces two types of outputs, files and metadata.
# - Files will be created under PIPELINE_ROOT directory.
# - Metadata will be written to SQLite database in METADATA_PATH.
PIPELINE_ROOT = os.path.join(OUTPUT_DIR, 'tfx_pipeline_output',
                             configs.PIPELINE_NAME)

METADATA_PATH = os.path.join(OUTPUT_DIR, 'tfx_metadata', configs.PIPELINE_NAME,
                             'metadata.db')

# The last component of the pipeline, "Pusher" will produce serving model under
# SERVING_MODEL_DIR.
SERVING_MODEL_DIR = os.path.join(PIPELINE_ROOT, 'serving_model')


def run():
  """Define a local pipeline."""

  orchestration.LocalDagRunner().run(
      run_pipeline.create_pipeline(
          pipeline_name=configs.PIPELINE_NAME,
          pipeline_root=PIPELINE_ROOT,
          data_path=configs.LOCAL_DATA_PATH,
          preprocessing_module=configs.LOCAL_TRANSFORM_MODULE_FILE,
          tuner_path=configs.LOCAL_TUNER_MODULE_PATH,
          training_module=configs.LOCAL_TRAIN_MODULE_FILE,
          serving_model_dir=SERVING_MODEL_DIR,
          metadata_connection_config=orchestration.metadata
          .sqlite_metadata_connection_config(METADATA_PATH)
          )
        )


if __name__ == '__main__':
  logging.set_verbosity(logging.INFO)
  run()