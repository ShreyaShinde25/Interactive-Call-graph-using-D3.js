

fetch('./example.json')
.then(function(resp){
    return resp.json();
})
.then(function(data){
    console.log("Test")
   parentFunction(data);
});


function createHierarchy(data) {
    let nodes = {};
    data.forEach(d => {
        let node = nodes[d.id] = nodes[d.id] || {};
        node.id=d.id;
        node.name = d.methodName;
        node.classPath = d.classPath;
        node.metrics = d.metrics;
        node.callees = d.callees;
        node.children = [];
    });

    data.forEach(d => {
        d.callees?.forEach(callee => {
            if (nodes[callee.id]) {
                nodes[d.id].children.push(nodes[callee.id]);
            }
        });
    });

    let rootNodes = Object.values(nodes).filter(node => !data.some(d => d.callees?.some(callee => callee.id === node.id)));
    return { name: "Root", children: rootNodes }; 
}



function calculateRadius(d) {
    // return d.data.callCount && d.data.callCount > 4 ? 28 : 12;
    if (d.data.size>10)
    {
        return d.data.size
    }
    else return 10;
   
}

function hotspotColor(d){
    // if(d.children == undefined){
    //     return 'white'
    // }

    if(d.data.callCount > 5)
    return 'maroon'
    else if (d.data.callCount>3 && d.data.callCount<=5)
    return 'red'
    else return 'yellow'

   
}

function parentFunction(jsondata){

let hierarchicalData = createHierarchy(jsondata);
let rootNode = d3.hierarchy(hierarchicalData, d => d.children);


console.log("the data is")
console.log(hierarchicalData)
console.log("HEYYY THEREEEEEEEE")
let mouseX = 0;
let buttonTracker = [];
// let rootNode = d3.hierarchy(jsondata, d=>d.children);
var pathLinks = rootNode.links(); 
var updatePathLinks;

var circleLinks = rootNode.descendants();
var updateCircleLinks;

var textLinks = rootNode.descendants();
var updateTextLinks;


let dim = {
    'width': window.screen.width/1.1, 
    'height':window.screen.height, 
    'margin':20    
};

let svg = d3.select('#chart').append('svg')
     .style('background', 'black')   
     .attrs(dim);


document.querySelector("#chart").classList.add("center");

//let rootNode = d3.hierarchy(data);


let g = svg.append('g') 
            .attr('transform', 'translate(140,50)');

    // let layout = d3.tree().size([dim.height-50, dim.width-320]);
    let layout = d3.tree().size([dim.width-320,dim.height-100]);
    layout(rootNode);
    console.log(rootNode.links());                   //-- this gives the source and targets 
    console.log("----------------------");
    console.log(rootNode.descendants());            // -- this gives the child data of every node.

    
    //console.log(rootNode.descendants());
   //first lets create a path 
   let lines = g.select('path');  



function update(data){

let group =  g.selectAll('path')
    // .data(data, (d,i) => d.target.data.name)
    .data(data, (d,i) => d.target.data.id)
    .join(
    function(enter){
        return enter.append('path')
                    .attrs({
                        'd': d3.linkVertical()
                        // .x(d => mouseX)
                        //  .y(d => d.x),
                         .x(d => d.x)
                         .y(d => mouseX),
                     'fill':'none',
                     'stroke':'white'
                    })
    },
    function(update){
        return update;
    },
    function(exit){
 


        return exit.call(path => path.transition().duration(300).remove()
                                                .attr('d', d3.linkVertical()
                                                            //   .x(d => mouseX)
                                                            //   .y(d =>d.x)
                                                              .x(d => d.x)
                                                              .y(d =>mouseX)));
    }


)
.call(path => path.transition().duration(1000).attr('d', d3.linkVertical()
        // .x(d => d.y)
        //  .y(d => d.x)
         .x(d => d.x)
         .y(d => d.y))
         .attr("id", function(d,i){return "path"+i}));


}


console.log("Path Links areee:-")
update(pathLinks); //rootNode.links()
console.log(pathLinks)



function updateCircles(data){
    g.selectAll('circle')
    // .data(data, (d) => d.data.name)
    .data(data, (d) => d.data.id)
    .join(
        function(enter){
            return enter.append('circle')
                        .attrs({
                            // 'cx':(d)=> mouseX,
                            // 'cy':(d) => d.x,
                            'cx':(d)=> d.x,
                            'cy':(d) => mouseX,
                            'r':(d) => calculateRadius(d),
                            'fill':(d) => hotspotColor(d),
                            // 'id': (d,i) =>d.data.name,
                            'id': (d,i) =>d.data.id,
                            'class':'sel'                           
                        })
        },
        function(update){
            return update
            .attr('r', (d) => calculateRadius(d)) // Fixed radius for update as well
            .attr('fill', (d)=> hotspotColor(d))
        },
        function(exit){

            return exit.call(path => path.transition().duration(300).remove()
            .attrs({
                // 'cx':(d) =>mouseX,
                'cy':(d) =>mouseX,
                'r':(d) => 0
            }));

        }


    )
    // .call(circle => circle.transition().duration(1000).attr('cx', (d)=>d.y))
    .call(circle => circle.transition().duration(1000).attr('cy', (d)=>d.y))
    .on('mouseover', function(d){

       d3.select(this)
           .attrs({                
               'fill': 'green',

           })
           .transition().duration(100).attrs({'r':(d) => calculateRadius(d)});
    })
    .on('mouseout', function(d){
       d3.select(this)
           .attr('fill', (d)=>hotspotColor(d))
           .transition().duration(100).attrs({'r':(d) => calculateRadius(d)});

    })
    .on('click', async function(d){

           let buttonId = d3.select(this)["_groups"][0][0]["attributes"].id.value;
           mouseX = d3.select(this)["_groups"][0][0]["attributes"].cy.value;
           //check to see if button already exists aka has been clicked
           //if it does, we need to send that data to update function
           //and remove that object

           let checkButtonExists = buttonTracker.filter(button => button.buttonId == buttonId);
 
           if(checkButtonExists[0]!=undefined){
                //also remove this item from button tracker
               buttonTracker = buttonTracker.filter(button => button.buttonId != buttonId);
               
               //handle path update
               pathLinks = checkButtonExists[0].buttonPathData.concat(pathLinks);
                              
               update(pathLinks);


                //handle  circle update
               circleLinks = checkButtonExists[0].buttonCircleData.concat(circleLinks);
                 updateCircles(circleLinks);

                 //handle text update

                textLinks =checkButtonExists[0].buttonTextData.concat(textLinks);
                updateText(textLinks);

                return;

           }
           var valueArray = await processedlinks(d.links());

           updatePathLinks = pathLinks.filter(function(item){        
                //    return !valueArray.includes(item.target.data.name)
                   return !valueArray.includes(item.target.data.id);                                       
           });

           //now run the filter to get unfiltered items
           var clickedPathData = pathLinks.filter(function(item){
            // return valueArray.includes(item.target.data.name)
            return valueArray.includes(item.target.data.id);
            });


           updateCircleLinks = circleLinks.filter(function(item){
                    // return !valueArray.includes(item.data.name)
                    return !valueArray.includes(item.data.id);
           });

           var clickedCircleData = circleLinks.filter(function(item){
                    // return valueArray.includes(item.data.name)
                    return valueArray.includes(item.data.id);
           });
        
        
           updateTextLinks = textLinks.filter(function(item){
                    // return !valueArray.includes(item.data.name)
                    return !valueArray.includes(item.data.id);
           });

           var clickedTextData = textLinks.filter(function(item){
                    // return valueArray.includes(item.data.name)
                    return valueArray.includes(item.data.id);
           });

           //now we push the circleData to an array
           buttonTracker.push({
               buttonId:buttonId,
               buttonPathData: clickedPathData,
               buttonCircleData:clickedCircleData,
               buttonTextData:clickedTextData
           })

           
           update(updatePathLinks);
           updateCircles(updateCircleLinks);
           updateText(updateTextLinks);
          async function processedlinks(dlinks) {
           var valueArray = [];
    
               return new Promise((resolve, reject)=>{
                     dlinks.forEach(async(element) =>{
                        //   valueArray.push(element.target.data.name)
                          valueArray.push(element.target.data.id); 
                     });
                     resolve(valueArray);      
               });
           }

           pathLinks = updatePathLinks;
           circleLinks = updateCircleLinks;
           textLinks = updateTextLinks;

    });


}

updateCircles(rootNode.descendants());
 

function updateText(data){
    let offset = 10
    g.selectAll('text')
    //   .data(data, (d) =>d.data.name)
      .data(data, (d) =>d.data.id)
      .join(
        function(enter){
            return enter.append('text')
                        .attrs({
                            
                            'x': (d) =>d.x + calculateRadius(d)+offset,
                            'y':(d) => mouseX ,
                            'font-size':0
                        })
                        // .text((d)=> {
                        //     let label = d.data.name;
                        //     if (d.data.callCount !== undefined) {
                        //         label += ` (Calls: ${d.data.callCount})`;
                        //     }
                        //     return label;
                        // })
                        
                        // .text((d) => d.data.name + (d.data.metrics?.length > 0 ? ` (${d.data.metrics[0].value})` : ''))
                        .text((d) => d.data.id + ' '+ d.data.classPath +'.' + d.data.name);
        },
        function(update){
            return update;
        },
        function(exit){
                return exit.call(text => text.transition().duration(300).remove().attrs({
                    //    'x':(d) => mouseX,
                       'y':(d) => mouseX,
                       'font-size':0
                }));   
        }

      )
      .call(text => text.transition().duration(1000).attrs({
        //   'x':(d) =>d.y+20,
          'y':(d) =>d.y+20,
          'font-size':20,
          'fill':'white',
        }));
}

updateText(textLinks);

}