import asyncio
import argparse
import yaml

from llmfilters.blocks.manager import BlockManager
from llmfilters.managers import get_manager

def run_pipeline(pipeline_file):
    with open(pipeline_file, 'r') as f:
        pipeline_config = yaml.safe_load(f)

    if 'manager' in pipeline_config:
        manager_config = pipeline_config['manager']
        manager_type = manager_config.get('type', None)

        try:
            manager_class = get_manager(manager_type)
            manager = manager_class(manager_config, pipeline_file)
            asyncio.run(manager.run())
        except Exception:
            raise
            print("Invalid manager type specified in the pipeline.yaml.")

    else:
        print("No manager specified in the pipeline.yaml.")

def main():
    parser = argparse.ArgumentParser(description='LLM Filters Pipeline')
    parser.add_argument('--pipeline-file', type=str, help='Path to the pipeline.yaml file')
    args = parser.parse_args()

    run_pipeline(args.pipeline_file)


if __name__ == '__main__':
    main()
