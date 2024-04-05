// create chart
document.addEventListener("DOMContentLoaded", function () {
  Highcharts.setOptions({
    colors: [
      "#7cb5ec",
      "#434348",
      "#90ed7d",
      "#f7a35c",
      "#8085e9",
      "#f15c80",
      "#e4d354",
      "#2b908f",
      "#f45b5b",
      "#91e8e1",
    ],
  });

  // Get the available years for plotting
  var years = eval(document.getElementById("model_years").innerHTML).map(function (x) { return parseInt(x); });
  // Sort the years
  years.sort(function (a, b) { return a - b; });
  // Get the year ticks and interval
  var year_ticks = years.length == 2 ? years : null;


  // Chart:economics_1_revenue_1_Irrigation_wide
  Highcharts.chart("economics_1_revenue_1_Irrigation_wide", {
    chart: {
      type: "column",
      marginRight: 200,
    },

    title: {
      text: "Revenue by Irrigation Status",
    },

    credits: {
      enabled: false,
    },

    series: JSON.parse(
      document.getElementById("economics_1_revenue_1_Irrigation_wide_csv").innerHTML
    ),

    xAxis: {
      tickPositions: year_ticks,
    },

    yAxis: {
      title: {
        text: "Revenue (billion AU$)",
      },
    },

    legend: {
      align: "right",
      verticalAlign: "left",
      layout: "vertical",
      x: -50,
      y: 300,
    },

    tooltip: {
      formatter: function () {
        return `<b>Year:</b> ${this.x}<br><b>${this.series.name
          }:</b>${this.y.toFixed(2)}<br/>`;
      },
    },

    plotOptions: {
      column: {
        stacking: "normal",
      },
    },

    exporting: {
      sourceWidth: 1200,
      sourceHeight: 600,
    },
  });

  // Chart:economics_1_revenue_2_Source_wide
  // Highcharts.chart("economics_1_revenue_2_Source_wide", {
  //   chart: {
  //     type: "column",
  //     marginRight: 200,
  //   },

  //   title: {
  //     text: "Revenue by Agricultural Product",
  //   },

  //   credits: {
  //     enabled: false,
  //   },

  //   data: {
  //     csv: document.getElementById("economics_1_revenue_2_Source_wide_csv")
  //       .innerHTML,
  //   },

  //   yAxis: {
  //     title: {
  //       text: "Revenue (billion AU$)",
  //     },
  //   },

  //   xAxis: {
  //     tickPositions: year_ticks,
  //   },

  //   legend: {
  //     align: "right",
  //     verticalAlign: "left",
  //     layout: "vertical",
  //     x: 10,
  //     y: 50,
  //   },

  //   tooltip: {
  //     formatter: function () {
  //       return `<b>Year:</b> ${this.x}<br><b>${
  //         this.series.name
  //       }:</b>${this.y.toFixed(2)}<br/>`;
  //     },
  //   },

  //   plotOptions: {
  //     column: {
  //       stacking: "normal",
  //     },
  //   },

  //   exporting: {
  //     sourceWidth: 1200,
  //     sourceHeight: 600,
  //   },
  // });

  // Chart:economics_1_revenue_3_Source_type_wide
  Highcharts.chart("economics_1_revenue_3_Source_type_wide", {
    chart: {
      type: "column",
      marginRight: 200,
    },

    title: {
      text: "Revenue by Agricultural Commodity",
    },

    credits: {
      enabled: false,
    },

    series: JSON.parse(
      document.getElementById("economics_1_revenue_3_Source_type_wide_csv").innerHTML
    ),

    yAxis: {
      title: {
        text: "Revenue (billion AU$)",
      },
    },

    xAxis: {
      tickPositions: year_ticks,
    },

    legend: {
      align: "right",
      verticalAlign: "left",
      layout: "vertical",
      x: 10,
      y: 50,
    },

    tooltip: {
      formatter: function () {
        return `<b>Year:</b> ${this.x}<br><b>${this.series.name
          }:</b>${this.y.toFixed(2)}<br/>`;
      },
    },

    plotOptions: {
      column: {
        stacking: "normal",
      },
    },

    exporting: {
      sourceWidth: 1200,
      sourceHeight: 600,
    },
  });


  // Chart:economics_1_revenue_4_Type_wide
  Highcharts.chart("economics_1_revenue_4_Type_wide", {
    chart: {
      type: "column",
      marginRight: 200,
    },

    title: {
      text: "Revenue by Commodity Type",
    },

    credits: {
      enabled: false,
    },

    series: JSON.parse(
      document.getElementById("economics_1_revenue_4_Type_wide_csv").innerHTML
    ),

    xAxis: {
      tickPositions: year_ticks,
    },

    yAxis: {
      title: {
        text: "Revenue (billion AU$)",
      },
    },

    legend: {
      align: "right",
      verticalAlign: "left",
      layout: "vertical",
      x: -50,
      y: 280,
    },

    tooltip: {
      formatter: function () {
        return `<b>Year:</b> ${this.x}<br><b>${this.series.name
          }:</b>${this.y.toFixed(2)}<br/>`;
      },
    },

    plotOptions: {
      column: {
        stacking: "normal",
      },
    },

    exporting: {
      sourceWidth: 1200,
      sourceHeight: 600,
    },
  });



  // Chart:economics_1_revenue_5_crop_lvstk_wide
  Highcharts.chart("economics_1_revenue_5_crop_lvstk_wide", {
    chart: {
      type: "column",
      marginRight: 200,
    },

    title: {
      text: "Revenue by Crop/Livestock",
    },

    series: JSON.parse(
      document.getElementById("economics_1_revenue_5_crop_lvstk_wide_csv").innerHTML
    ),

    credits: {
      enabled: false,
    },

    yAxis: {
      title: {
        text: "Revenue (billion AU$)",
      },
    },
    xAxis: {
      tickPositions: year_ticks,
    },

    legend: {
      align: "right",
      verticalAlign: "left",
      layout: "vertical",
      x: -50,
      y: 280,
    },

    tooltip: {
      formatter: function () {
        return `<b>Year:</b> ${this.x}<br><b>${this.series.name
          }:</b>${this.y.toFixed(2)}<br/>`;
      },
    },

    plotOptions: {
      column: {
        stacking: "normal",
      },
    },

    exporting: {
      sourceWidth: 1200,
      sourceHeight: 600,
    },
  });

  // Chart:economics_2_cost_1_Irrigation_wide
  Highcharts.chart("economics_2_cost_1_Irrigation_wide", {
    chart: {
      type: "column",
      marginRight: 200,
    },

    title: {
      text: "Cost of Production by Irrigation Status",
    },

    credits: {
      enabled: false,
    },

    series: JSON.parse(
      document.getElementById("economics_2_cost_1_Irrigation_wide_csv").innerHTML
    ),

    yAxis: {
      title: {
        text: "Cost (billion AU$)",
      },
    },
    xAxis: {
      tickPositions: year_ticks,
    },

    legend: {
      align: "right",
      verticalAlign: "left",
      layout: "vertical",
      x: -50,
      y: 300,
    },

    tooltip: {
      formatter: function () {
        return `<b>Year:</b> ${this.x}<br><b>${this.series.name
          }:</b>${this.y.toFixed(2)}<br/>`;
      },
    },

    plotOptions: {
      column: {
        stacking: "normal",
      },
    },

    exporting: {
      sourceWidth: 1200,
      sourceHeight: 600,
    },
  });

  // Chart:economics_2_cost_2_Source_wide
  Highcharts.chart("economics_2_cost_2_Source_wide", {
    chart: {
      type: "column",
      marginRight: 200,
    },

    title: {
      text: "Cost of Production by Agricultural Land-use",
    },

    credits: {
      enabled: false,
    },

    series: JSON.parse(
      document.getElementById("economics_2_cost_2_Source_wide_csv").innerHTML
    ),

    yAxis: {
      title: {
        text: "Cost (billion AU$)",
      },
    },
    xAxis: {
      tickPositions: year_ticks,
    },

    legend: {
      align: "right",
      verticalAlign: "left",
      layout: "vertical",
      x: 10,
      y: 80,
    },

    tooltip: {
      formatter: function () {
        return `<b>Year:</b> ${this.x}<br><b>${this.series.name
          }:</b>${this.y.toFixed(2)}<br/>`;
      },
    },

    plotOptions: {
      column: {
        stacking: "normal",
      },
    },

    exporting: {
      sourceWidth: 1200,
      sourceHeight: 600,
    },
  });

  // // Chart:economics_2_cost_3_Source_type_wide
  // Highcharts.chart('economics_2_cost_3_Source_type_wide', {

  //     chart: {
  //         type: 'column',
  //         marginRight: 200
  //     },

  //     title: {
  //         text: 'Cost of Production by Commodity'
  //     },

  //     credits: {
  //         enabled: false
  //     },

  //     data: {
  //         csv: document.getElementById('economics_2_cost_3_Source_type_wide_csv').innerHTML,
  //     },

  //     yAxis: {
  //         title: {
  //             text: 'Cost (billion AU$)'
  //         },
  //     },xAxis: {
  //     tickPositions: tickposition
  // },

  //     legend: {
  //         align: 'right',
  //         verticalAlign: 'left',
  //         layout: 'vertical',
  //         x: 80,
  //         y: 10

  //     },

  //     tooltip: {
  //         formatter: function () {
  //             return `<b>Year:</b> ${this.x}<br><b>${this.series.name}:</b>${this.y.toFixed(2)}<br/>`;
  //         }
  //     },

  //     plotOptions: {
  //         column: {
  //             stacking: 'normal',
  //         }
  //     },

  //     exporting: {
  //         sourceWidth: 1200,
  //         sourceHeight: 600,
  //     }
  // });

  // Chart:economics_2_cost_4_Type_wide
  Highcharts.chart("economics_2_cost_4_Type_wide", {
    chart: {
      type: "column",
      marginRight: 200,
    },

    title: {
      text: "Cost of Production by Commodity Type",
    },

    credits: {
      enabled: false,
    },

    series: JSON.parse(
      document.getElementById("economics_2_cost_4_Type_wide_csv").innerHTML
    ),

    yAxis: {
      title: {
        text: "Cost (billion AU$)",
      },
    },
    xAxis: {
      tickPositions: year_ticks,
    },

    legend: {
      align: "right",
      verticalAlign: "left",
      layout: "vertical",
      x: -50,
      y: 280,
    },

    tooltip: {
      formatter: function () {
        return `<b>Year:</b> ${this.x}<br><b>${this.series.name
          }:</b>${this.y.toFixed(2)}<br/>`;
      },
    },

    plotOptions: {
      column: {
        stacking: "normal",
      },
    },

    exporting: {
      sourceWidth: 1200,
      sourceHeight: 600,
    },
  });

  // Chart:economics_2_cost_5_crop_lvstk_wide
  Highcharts.chart("economics_2_cost_5_crop_lvstk_wide", {
    chart: {
      type: "column",
      marginRight: 200,
    },

    title: {
      text: "Cost of Production by Crop/Livestock",
    },

    series: JSON.parse(
      document.getElementById("economics_2_cost_5_crop_lvstk_wide_csv").innerHTML
    ),

    credits: {
      enabled: false,
    },

    yAxis: {
      title: {
        text: "Cost (billion AU$)",
      },
    },

    xAxis: {
      tickPositions: year_ticks,
    },

    legend: {
      align: "right",
      verticalAlign: "left",
      layout: "vertical",
      x: -50,
      y: 280,
    },

    tooltip: {
      formatter: function () {
        return `<b>Year:</b> ${this.x}<br><b>${this.series.name
          }:</b>${this.y.toFixed(2)}<br/>`;
      },
    },

    plotOptions: {
      column: {
        stacking: "normal",
      },
    },

    exporting: {
      sourceWidth: 1200,
      sourceHeight: 600,
    },
  });

  // Chart:economics_3_rev_cost_all

  Highcharts.chart("economics_3_rev_cost_all", {

    chart: {
      type: "columnrange",
      marginRight: 200,
    },

    title: {
      text: "Agricultural Revenue and Cost of Production",
    },

    credits: {
      enabled: false,
    },

    series:
      JSON.parse(
        document.getElementById("economics_3_rev_cost_all_csv").innerText
      )['series']
    ,

    xAxis: {
      categories: JSON.parse(
        document.getElementById("economics_3_rev_cost_all_csv").innerText
      )['categories'],
    },

    yAxis: {
      title: {
        text: "Value (billion AU$)",
      },
    },

    tooltip: {
      formatter: function () {
        return (
          "<b>" +
          this.series.name +
          "</b>: " +
          Highcharts.numberFormat(this.point.low, 2) +
          " - " +
          Highcharts.numberFormat(this.point.high, 2) +
          " (billion AU$)"
        );
      },
    },

    plotOptions: {
      columnrange: {
        borderRadius: "50%",
      },
    },

    legend: {
      align: "right",
      verticalAlign: "left",
      layout: "vertical",
      x: -50,
      y: 280,
    },
  });


});

