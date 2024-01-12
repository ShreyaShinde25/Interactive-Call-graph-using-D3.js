# Interactive-Call-graph-using-D3.js

## Input Data Format
- Input data should be as a **list** in JSON format
- Each method in the input data should have attributes in the following structure:

```
{
  "id": 0,
  "classPath": "",
  "methodName": "",
  "metrics": [
    {
      "key": "",
      "value": 0
    }
  ],
  "callees": [
    {
      "id": 0,
      "callCount": 0
    }
  ]
}

```
- Attribute details:
  - ```id```: unique identifier for the current method
  - ```classPath```: the Java classPath for the current method (```classPath```.```methodName``` should also be able to uniquely identify the current method)
  - ```methodName```: the name of the current method
  - ```metrics```: a list of collected metrics for the current method in key-value format
    - ```key```: the name of the metric collected 
    - ```value```: the value corresponding to a particular metric  
  - ```callees```: a list of callee methods called by the current method
    - ```id```: unique identifier for the callee method
    - ```callCount```: the amount of times the callee method is called by the current method

- The following keys are currently supported:
  - **methodSize**: the size of the method in bytecode

- See ```example.json``` for reference

