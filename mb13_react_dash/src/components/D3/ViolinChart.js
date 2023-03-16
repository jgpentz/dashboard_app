import * as d3 from "d3";
import * as d3Collection from 'd3-collection';

export default function ViolinChart(config = {}) {
    var margin = config.margin || { top: 50, bottom: 50, left: 50, right: 50 },
        // width = config.width ? config.width - margin.left - margin.right : 900 - margin.left - margin.right,
        // height = config.height ? config.height - margin.top - margin.bottom : 900 -margin.top - margin.bottom,
        height = config.height,
        width = config.width,
        id = config.id,
        data = config.data ? config.data : [],
        svg,
        drawChart,
        updateScales,
        x,
        y,
        chartArea,
        firstRender = true,
        drawLegend,
        filteredData,
        xAxisCall,
        yAxisCall,
        x_axis,
        y_axis,
        size = config.size,
        histogram




        x = d3.scaleBand().padding(0.08)
        y = d3.scaleLinear()

        x_axis = d3.axisBottom()
        y_axis = d3.axisLeft()

        var xNum = d3.scaleLinear()

    function chart(selection){
        selection.each(function() {
            // Refer to the attached DOM element.
            var dom = d3.select(this);
            svg = dom.select('svg')
                .attr('id', id)
                .append('g')
            chartArea = svg.append('g').attr('id', 'chart-' + id)
                .attr('transform', 'translate(' + margin.left + ',' + margin.top + ')')

            xAxisCall = chartArea.append('g')
                .attr('class', 'axis')

            yAxisCall = chartArea.append('g')
                .attr('class', 'axis')


            updateScales = (ticks) => {
                let groupedData = d3Collection.nest()
                    .key(d=> d.week)
                    .entries(data)

                x.domain(groupedData.map(d=> d.key))
                    .range([0, width])

                let yMax = d3.max(groupedData, d=> d3.max(d.values, v=> v.gain))
                let yMin = d3.min(groupedData, d=> d3.min(d.values, v=> v.gain))

                y.domain([yMin * 0.95, yMax * 1.05])
                    .range([height, 0])

                x_axis.scale(x);
                y_axis.scale(y).ticks(5);

                xAxisCall
                    .attr('transform', 'translate(0,' + height + ')')
                    .call(x_axis)

                yAxisCall.call(y_axis);

                histogram = d3.bin()
                    .domain(y.domain())
                    .thresholds(y.ticks(20))
                    .value(d=>d)

                filteredData = d3Collection.nest()
                    .key(function(d){ return d.week})
                    .rollup(function(d){
                        var input = d.map( g => g.gain );
                        var bins = histogram(input)
                        return(bins)
                    })
                    .entries(data);

                var maxNum = 0;
                for (var i in filteredData) {
                    let allBins = filteredData[i].value
                    let lengths = allBins.map(a=> a.length);
                    let longest = d3.max(lengths);
                    if (longest > maxNum) { maxNum = longest}
                }

                xNum.range([0, x.bandwidth()])
                    .domain([-maxNum, maxNum])


            }

            drawChart = (resizing = false) =>{

                let violins = chartArea.selectAll('.violins')
                    .data(filteredData, d=> d.key)

                violins.exit().remove()

                let test = violins.enter()
                    .append('g')
                    .attr('class', 'violins')
                    .attr('transform', function(d){
                        return ("translate(" + x(d.key) + " ,0)");
                    })
                    .append('path')
                        .datum(function(d){
                            return d.value;
                        })

                        .style('stroke', 'none')
                        .style('fill', '#69b3a2')
                        .attr('d', d3.area()
                            .x0(d=> {
                                return xNum(-d.length)})
                            .x1(d=> xNum(d.length))
                            .y(d=> y(d.x0))
                            .curve(d3.curveCatmullRom)
                        )


                firstRender = false
            }

            drawLegend = () => {

            }
        });
    }

    chart.data = function(value) {
        if (!arguments.length) return data;
        data=value;
        if (!data) return;
        updateScales();
        drawChart(false);

        return chart;
    }

    chart.width = function(value) {
        if (!arguments.length) return width;
        width = value;
        return chart;
    }

    chart.height = function(value) {
        if (!arguments.length) return height;
        height = value;
        return chart;
    }

    chart.size = function(w, h){
        if (!arguments.length) return {width: width, height: height}
        chart.width(w - margin.left - margin.right);
        chart.height(h - margin.top - margin.bottom);

        if (!data) return;
        updateScales();
        if (firstRender) {
            drawChart(true);
        }
        return chart;
    }

    return chart;
}