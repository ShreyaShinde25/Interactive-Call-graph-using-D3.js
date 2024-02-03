# Interactive-Call-graph-using-D3.js

## Input Data Format (*Per Graph*)
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
  - ```className```: the Java classPath for the current method (```className```.```methodName``` should also be able to uniquely identify the current method)
  - ```methodName```: the name of the current method
  - ```metrics```: a list of collected metrics for the current method in key-value format
    - ```key```: the name of the metric collected 
    - ```value```: the value corresponding to a particular metric  
  - ```callees```: a list of callee methods called by the current method
    - ```id```: unique identifier for the callee method
    - ```callCount```: the amount of times the callee method is called by the current method

- The following keys are currently supported:
  - **methodSize**: the size of the method in bytecode

### Execution Paths
- Each execution path should be stored in the following **nested/recursive** structure
```
{
  "id": string,
  "children": 
  [
    {
      "id": string,
      "children": 
      [
        {
          "id": string,
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
  - ```children```: a list of methods that fall under the current execution path (defined recursively). The last node in the execution path should have an empty list for its children
    - A new child should only be added under the parent when the child is called by the parent from a unique position (i.e. line number) in the code for the **first time**
    - For recursive methods, this may mean the recursion stops after just one child is added (i.e. this means the recursive call is only made from a single position in the method)


- See ```example.json``` for reference

