from pathlib import Path

import yaml

with open('../configuration.yml', mode='r') as conf_file:
    conf = yaml.safe_load(conf_file)

conf['root_path'] = Path(conf['root_path']).resolve()  # type: Path
