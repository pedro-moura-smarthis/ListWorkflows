import xml.etree.ElementTree as ET
import os
import pandas as pd
import logging


def ReadXmlAsObject(filePath: str) -> ET.ElementTree:
    logging.info(f"Generating the ElementTree object for the {filePath}")
    tree : ET.ElementTree = ET.parse(filePath)
    root : ET.ElementTree = tree.getroot()
    return root


def IterateOverXmlTree(file_path : str,
                        projectFolder : str,
                        namespace="{http://schemas.microsoft.com/netfx/2009/xaml/activities}") -> pd.DataFrame:

    listedWorkflows = {"state":[],
            "workflowId": [],
            "filePath": [],
            "annotation": []}
    logging.info(f"Creating a DataFrame to keep information of the workflows inside the file")
    listedWorkflows = pd.DataFrame(listedWorkflows)
    root = ReadXmlAsObject(file_path)
    for parent_element in root.iter(f"{namespace}State"):
        state = parent_element.attrib['DisplayName']
        listedWorkflows = GetInvokeWorkflowFileName(listedWorkflows,
                                    parent_element,
                                    projectFolder,
                                    state)
    return listedWorkflows


def GetInvokeWorkflowFileName(listedWorkflows : pd.DataFrame,
                            root : ET.ElementTree,
                            projectFolder : str,
                            state : str,
                            namespace="{http://schemas.uipath.com/workflow/activities}") -> pd.DataFrame:

    workflowTagToIterate = list(root.iter(f"{namespace}InvokeWorkflowFile"))
    numberOfInvokes = len(workflowTagToIterate)

    if numberOfInvokes == 0:
        logging.debug(f"The current file there is no InvokesWorkflows. Returning None.")
        return listedWorkflows
    
    logging.debug(f"There is {len(workflowTagToIterate)} Invokes to iterate.")

    for parent_element in workflowTagToIterate:
        filePath = os.path.join(*parent_element.attrib['WorkflowFileName'].split('\\'))
        workflowIdRef = parent_element.attrib["{http://schemas.microsoft.com/netfx/2010/xaml/activities/presentation}WorkflowViewState.IdRef"]

        try:
            annotation = parent_element.attrib["{http://schemas.microsoft.com/netfx/2010/xaml/activities/presentation}Annotation.AnnotationText"].replace(",","").replace("\n","")
        except:
            logging.debug(f"The current invokeWorkflow do not have a annotation. Seeting default value")
            annotation = "Nothing"

        infoToAdd = [state, workflowIdRef, filePath, annotation]

        logging.info(f"Filling the DataFrame with the info of the current invokeWorkflow [{filePath}]")
        logging.debug(f"{infoToAdd}")
        listedWorkflows.loc[len(listedWorkflows)] = infoToAdd
        file_path = os.path.normpath(os.path.join(projectFolder, filePath))
        listedWorkflows = GetInvokeWorkflowFileName(listedWorkflows,
                                    ReadXmlAsObject(file_path), 
                                    projectFolder, 
                                    state)
    return listedWorkflows
        
