import os
import logging
import pandas as pd
from datetime import datetime

import Functions.GetProjectWorkflows
import Functions.ReadConfig

def main():

    config = Functions.ReadConfig.ReadConfig("projectConfig.json")
    mainPath = config["mainPath"]
    projectFolder = os.path.dirname(mainPath)
    projectName = os.path.basename(projectFolder)
    logging.basicConfig(filename=f"{projectName}_{datetime.now()}.log",
                        level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(message)s')
    logging.info(f"Starting the process of listing all workflows of the {projectName}")
    workFlows : pd.DataFrame  = Functions.GetProjectWorkflows.IterateOverXmlTree(mainPath, projectFolder)
    workFlows= workFlows.iloc[::-1]
    workFlows = workFlows.drop_duplicates(subset=['workflowId', 'filePath']).reset_index(drop = True)
    workFlows["folder"] = workFlows["filePath"].apply(os.path.dirname)
    workFlows["fileName"] = workFlows["filePath"].apply(os.path.basename)
    workFlows.to_csv(f"{projectName}.csv",
                     index=False,
                     lineterminator="\r")

if __name__ == "__main__":
    main()
