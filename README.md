# Interactive-Call-graph-using-D3.js


## Project Setup (Optional)

Download the latest release of the Dacapo benchmark mark from: https://github.com/dacapobench/dacapobench/releases. 
The downloaded .zip file should be extracted to the directory `preprocessing/apps`. There should be 2 main components extracted:
- A folder named `dacapo-***/`
- A jar file named ` dacapo-***.jar`

## Example

### Visualization Input Data Generation (HelloWorld)
1. Navigate to the directory `preprocessing/scripts`
2. Run the script named `gen_hello.sh` (which runs a HelloWorld program)
3. Visualization input data for the HelloWorld program should be available in the directory `preprocessing/out` with the names `hello_trace_***.json`


### Visualization Input Data Generation (Dacapo)
0. Download the Dacapo benchmark based on instructions from [Project Setup](#project-setup-(optional)).
1. Navigate to the directory `preprocessing/scripts`
2. Run the script named `gen_dacapo.sh <benchmark_name>` (which runs a Dacapo benchmark)
3. Visualization input data for the benchmark program should be available in the directory `preprocessing/out` with the names `<benchmark_name>_trace_***.json`

## Visualization Input Data Format (*Per Graph*)
- Input data should be as a **list** in JSON format
- Input data should be divided into 2 sections ```methods``` and ```paths```
```
{
  methods: [list of method objects],
  paths: [list of unique execution paths]
}
```
### Method Objects
- Each ```method object``` in the input data should have attributes in the following structure:

```
{
  "id": string,
  "className": string,
  "methodName": string,
  "methodDescriptor" string,
  "metrics": [
    {
      "key": string,
      "value": numeric
    }, 
    {
      "key": string,
      "value": numeric
    },
    ...
  ],
}

```
- Attribute details:
  - ```id```: unique identifier for the current method
  - ```className```: the Java classPath for the current method (```className```.```methodName``````methodDescriptor``` should also be able to uniquely identify the current method)
  - ```methodName```: the name of the current method
  - ```methodDescriptor```: the input type(s) and return type of the current method
  - ```metrics```: a list of collected metrics for the current method in key-value format
    - ```key```: the name of the metric collected 
    - ```value```: the value corresponding to a particular metric  
  - ```callees```: a list of callee methods called by the current method
    - ```id```: unique identifier for the callee method
    - ```callCount```: the amount of times the callee method is called by the current method

- The following keys are currently supported:
  - **methodSize**: the size of the method in bytecode
  - **cpu**: the cpu util % of the method (WIP)

### Execution Paths
- Each execution path should be stored in the following **nested/recursive** structure
```
{
  "id": string,
  "callSite": string,
  "execType": string,
  "children": 
  [
    {
      "id": string,
      "callSite": string,
      "execType": string,
      "children": 
      [
        {
          "id": string,
          "callSite": string,
          "execType": string,
          "children": 
          [
            ...
          ]
        },
        ...
      ]
    },
    ...
  ]
}

```
- Attribute details:
  - ```id```: unique identifier for the current method in the execution path (this should be the same id that uniquely identifies a method object)
  - ```callSite```: the location (in terms of bytecode index) in the caller (parent) method that called the current method. For the first entry in the path, this value is the Java Thread for which the stack belongs to
  - ```execType```: the execution type for this invocation (i.e. interpretted, compiled, or native)
  - ```children```: a list of methods that fall under the current execution path (defined recursively). The last node in the execution path should have an empty list for its children
    - A new child should only be added under the parent when the child is called by the parent from a unique position (i.e. line number) in the code for the **first time**
    - For recursive methods, this may mean the recursion stops after just one child is added (i.e. this means the recursive call is only made from a single position in the method)


- See ```example.json``` for reference

