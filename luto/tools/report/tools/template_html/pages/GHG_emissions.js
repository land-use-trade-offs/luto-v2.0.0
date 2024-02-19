// make charts
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

  // Get the years from the csv
  var tickposition;
  $(document).ready(function () {
    let csv, csv_lines;
    let years = [];

    csv = document.getElementById(
      "GHG_1_cunsum_emission_Mt_csv"
    ).innerHTML;
    
    csv_lines = csv.split("\n");

    // if the last line is empty, remove it
    if (csv_lines[csv_lines.length - 1] == "") {
      csv_lines.pop();
    }

    $.each(csv_lines, function (lineNo, line) {
      var items = line.split(",");

      if (lineNo != 0) {
        // Skip the first line (headers)
        years.push(parseFloat(items[0]));
      }
    });

    // if the length of the years is greater than 5, then set the tickposition = bull
    if (years.length < 5) {
      tickposition = years;
    } else {
      tickposition = null;
    }

    // Chart:GHG_1_cunsum_emission_Mt
    Highcharts.chart("GHG_1_cunsum_emission_Mt", {
      chart: {
        type: "column",
        marginRight: 200,
      },

      title: {
        text: "Net Land Sector GHG Emissions",
      },

      credits: {
        enabled: false,
      },

      data: {
        csv: document.getElementById("GHG_1_cunsum_emission_Mt_csv").innerHTML,
      },

      yAxis: {
        title: {
          text: "Greenhouse Gas (Mt CO2e)",
        },
      },
      xAxis: {
        tickPositions: tickposition,
      },

      legend: {
        enabled: false,
        // align: 'right',
        // verticalAlign: 'top',
        // layout: 'vertical',
        // x: 10,
        // y: 50
      },

      tooltip: {
        formatter: function () {
          return `<b>Year:</b> ${this.x}<br><b>${
            this.series.name
          }:</b>${this.y.toFixed(2)}<br/>`;
        },
      },

      plotOptions: {
        column: {
          stacking: "normal",
          dataLabels: {
            enabled: false,
          },
        },
      },

      exporting: {
        sourceWidth: 1200,
        sourceHeight: 600,
      },
    });

    // Chart:GHG_2_individual_emission_Mt
    let options = {
      chart: {
        renderTo: "GHG_2_individual_emission_Mt",
        marginRight: 200,
      },
      title: {
        text: "GHG Emissions by Land-use/Management Type",
      },

      xAxis: {
        categories: [],
      },

      yAxis: {
        title: {
          text: "Greenhouse Gas (Mt CO2e)",
        },
      },
      legend: {
        align: "right",
        verticalAlign: "top",
        layout: "vertical",
        x: 10,
        y: 250,
      },
      tooltip: {
        formatter: function () {
          return `<b>Year:</b> ${this.x}<br><b>${
            this.series.name
          }:</b>${this.y.toFixed(2)}<br/>`;
        },
      },
      series: [
        {
          name: "Series 0",
          data: [],
          type: "column",
        },
        {
          name: "Series 1",
          data: [],
          type: "column",
        },
        {
          name: "Series 2",
          data: [],
          type: "column",
        },
        {
          name: "Series 3",
          data: [],
          type: "column",
        },
        {
          name: "Series 4",
          data: [],
          type: "spline",
        },
      ],
      credits: {
        enabled: false,
      },
      plotOptions: {
        column: {
          stacking: "normal",
          dataLabels: {
            enabled: false,
          },
        },
      },
      exporting: {
        sourceWidth: 1200,
        sourceHeight: 600,
      },
    };

    // push data into options
    let data = document.getElementById(
      "GHG_2_individual_emission_Mt_csv"
    ).innerHTML;
    // Split the lines
    var lines = data.split("\n");
    // If the last line is empty, remove it
    if (lines[lines.length - 1] == "") {
      lines.pop();
    }

    // Push column data into data list
    for (let i = 0; i < lines.length; i++) {
      if (i == 0) {
        // push column names into series names
        options.series[0].name = lines[i].split(",")[1];
        options.series[1].name = lines[i].split(",")[2];
        options.series[2].name = lines[i].split(",")[3];
        options.series[3].name = lines[i].split(",")[4];
        options.series[4].name = lines[i].split(",")[5];
      } else {
        // push row data into series data
        let year = lines[i].split(",")[0];
        let col1 = lines[i].split(",")[1];
        let col2 = lines[i].split(",")[2];
        let col3 = lines[i].split(",")[3];
        let col4 = lines[i].split(",")[4];
        let col5 = lines[i].split(",")[5];

        options.xAxis.categories.push(parseFloat(year));
        options.series[0].data.push(parseFloat(col1));
        options.series[1].data.push(parseFloat(col2));
        options.series[2].data.push(parseFloat(col3));
        options.series[3].data.push(parseFloat(col4));
        options.series[4].data.push(parseFloat(col5));
      }
    }

    // Create the chart
    var chart = new Highcharts.Chart(options);

    // Chart:GHG_3_crop_lvstk_emission_Mt
    Highcharts.chart("GHG_3_crop_lvstk_emission_Mt", {
      chart: {
        type: "column",
        marginRight: 200,
      },

      title: {
        text: "GHG Emissions by Crop/Livestock",
      },

      credits: {
        enabled: false,
      },

      data: {
        csv: document.getElementById("GHG_3_crop_lvstk_emission_Mt_csv")
          .innerHTML,
      },

      yAxis: {
        title: {
          text: "Greenhouse Gas (Mt CO2e)",
        },
      },
      xAxis: {
        tickPositions: tickposition,
      },

      legend: {
        align: "right",
        verticalAlign: "top",
        layout: "vertical",
        x: 10,
        y: 250,
      },

      tooltip: {
        formatter: function () {
          return `<b>Year:</b> ${this.x}<br><b>${
            this.series.name
          }:</b>${this.y.toFixed(2)}<br/>`;
        },
      },

      plotOptions: {
        column: {
          stacking: "normal",
          dataLabels: {
            enabled: false,
          },
        },
      },

      exporting: {
        sourceWidth: 1200,
        sourceHeight: 600,
      },
    });

    // Chart:GHG_4_dry_irr_emission_Mt
    Highcharts.chart("GHG_4_dry_irr_emission_Mt", {
      chart: {
        type: "column",
        marginRight: 200,
      },

      title: {
        text: "GHG Emissions by Irrigation Type",
      },

      credits: {
        enabled: false,
      },

      data: {
        csv: document.getElementById("GHG_4_dry_irr_emission_Mt_csv").innerHTML,
      },

      yAxis: {
        title: {
          text: "Greenhouse Gas (Mt CO2e)",
        },
      },
      xAxis: {
        tickPositions: tickposition,
      },

      legend: {
        align: "right",
        verticalAlign: "top",
        layout: "vertical",
        x: -50,
        y: 250,
      },

      tooltip: {
        formatter: function () {
          return `<b>Year:</b> ${this.x}<br><b>${
            this.series.name
          }:</b>${this.y.toFixed(2)}<br/>`;
        },
      },

      plotOptions: {
        column: {
          stacking: "normal",
          dataLabels: {
            enabled: false,
          },
        },
      },

      exporting: {
        sourceWidth: 1200,
        sourceHeight: 600,
      },
    });

    // Chart:GHG_5_category_emission_Mt
    Highcharts.chart("GHG_5_category_emission_Mt", {
      chart: {
        type: "column",
        marginRight: 200,
      },

      title: {
        text: "GHG Emissions by Gas",
      },

      credits: {
        enabled: false,
      },

      data: {
        csv: document.getElementById("GHG_5_category_emission_Mt_csv")
          .innerHTML,
      },

      yAxis: {
        title: {
          text: "Greenhouse Gas (Mt CO2e)",
        },
      },
      xAxis: {
        tickPositions: tickposition,
      },

      legend: {
        align: "right",
        verticalAlign: "top",
        layout: "vertical",
        x: 0,
        y: 250,
      },

      tooltip: {
        formatter: function () {
          return `<b>Year:</b> ${this.x}<br><b>${
            this.series.name
          }:</b>${this.y.toFixed(2)}<br/>`;
        },
      },

      plotOptions: {
        column: {
          stacking: "normal",
          dataLabels: {
            enabled: false,
          },
        },
      },

      exporting: {
        sourceWidth: 1200,
        sourceHeight: 600,
      },
    });

    // Chart:GHG_6_sources_emission_Mt
    Highcharts.chart("GHG_6_sources_emission_Mt", {
      chart: {
        type: "column",
        marginRight: 200,
        marginBottom: 200,
      },

      title: {
        text: "GHG Emissions by Source",
      },

      credits: {
        enabled: false,
      },

      data: {
        csv: document.getElementById("GHG_6_sources_emission_Mt_csv").innerHTML,
      },

      yAxis: {
        title: {
          text: "Emissions (Mt CO2e)",
        },
      },
      xAxis: {
        tickPositions: tickposition,
      },

      // legend: {
      //     // itemStyle: {
      //     //     "fontSize": "6px",
      //     //     "textOverflow": "ellipsis",
      //     // },
      //     align: 'bottom',
      //     // verticalAlign: 'top',
      //     // layout: 'vertical',
      //     x: 80,
      //     y: 0
      // },

      tooltip: {
        formatter: function () {
          return `<b>Year:</b> ${this.x}<br><b>${
            this.series.name
          }:</b>${this.y.toFixed(2)}<br/>`;
        },
      },

      plotOptions: {
        column: {
          stacking: "normal",
          dataLabels: {
            enabled: false,
          },
        },
      },

      exporting: {
        sourceWidth: 1200,
        sourceHeight: 600,
      },
    });

    // Chart:GHG_7_lu_lm_emission_Mt_wide
    let GHG_7_lu_lm_emission_Mt_wide_option = {
      chart: {
        renderTo: "GHG_7_lu_lm_emission_Mt_wide",
        marginRight: 200,
      },
      title: {
        text: "GHG Emissions - Start and End Year",
      },
      xAxis: {
        categories: [],
      },

      yAxis: {
        title: {
          text: "Greenhouse Gas (t CO2e/ha)",
        },
      },
      legend: {
        align: "right",
        verticalAlign: "top",
        layout: "vertical",
        x: -10,
        y: 200,
      },
      tooltip: {
        formatter: function () {
          return `<b>Year:</b> ${this.x}<br><b>${
            this.series.name
          }:</b>${this.y.toFixed(2)}<br/>`;
        },
      },
      series: [
        {
          name: "Series 0",
          data: [],
          type: "column",
          stack: "",
        },
        {
          name: "Series 1",
          data: [],
          type: "column",
          stack: "",
        },
        {
          name: "Series 2",
          data: [],
          type: "column",
          stack: "",
        },
        {
          name: "Series 3",
          data: [],
          type: "column",
          stack: "",
        },
      ],

      credits: {
        enabled: false,
      },

      plotOptions: {
        column: {
          stacking: "normal",
          dataLabels: {
            enabled: false,
          },
        },
      },
      exporting: {
        sourceWidth: 1200,
        sourceHeight: 600,
      },
    };

    // Assuming the CSV has a header row and multiple data rows matching the series array length
    let inner_txt = $("#GHG_7_lu_lm_emission_Mt_wide_csv").html();
    var lines = inner_txt.split("\n");

    // Set categories from the first line (header)
    GHG_7_lu_lm_emission_Mt_wide_option.xAxis.categories = lines[0]
      .split(",")
      .slice(2);

    // Process each line (excluding the header)
    for (let i = 1; i < lines.length; i++) {
      let lineData = lines[i].split(",");
      if (GHG_7_lu_lm_emission_Mt_wide_option.series[i - 1]) {
        GHG_7_lu_lm_emission_Mt_wide_option.series[i - 1].stack = lineData[0];
        GHG_7_lu_lm_emission_Mt_wide_option.series[i - 1].name = lineData[1];
        GHG_7_lu_lm_emission_Mt_wide_option.series[i - 1].data = lineData
          .slice(2)
          .map((x) => parseFloat(x));
      }
    }

    var chart = new Highcharts.Chart(GHG_7_lu_lm_emission_Mt_wide_option);

    // Chart:GHG_8_lu_source_emission_Mt
    Highcharts.chart("GHG_8_lu_source_emission_Mt", {
      chart: {
        type: "packedbubble",
      },
      title: {
        text: "GHG Emissions in the target year",
      },
      tooltip: {
        useHTML: true,
        pointFormat: "<b>{point.name}:</b> {point.value}m CO<sub>2</sub>",
      },
      plotOptions: {
        packedbubble: {
          useSimulation: true,
          splitSeries: false,
          minSize: "10%",
          maxSize: "1000%",
          dataLabels: {
            enabled: true,
            format: "{point.name}",
            filter: {
              property: "y",
              operator: ">",
              value: 1,
            },
          },
        },
      },

      series: JSON.parse($("#GHG_8_lu_source_emission_Mt_csv").html()),

      credits: {
        enabled: false,
      },

      exporting: {
        sourceWidth: 1200,
        sourceHeight: 600,
      },
    });

    // Chart:GHG_9_1_ag_reduction_total_wide_Mt
    // Highcharts.chart('GHG_9_1_ag_reduction_total_wide_Mt', {
    //     chart: {
    //         type: 'column',
    //         marginRight: 200
    //     },

    //     title: {
    //         text: 'Non Agricultural Land-use Sequestration in total'
    //     },

    //     credits: {
    //         enabled: false
    //     },

    //     data: {
    //         csv: document.getElementById('GHG_9_1_ag_reduction_total_wide_Mt_csv').innerHTML,
    //     },

    //     yAxis: {
    //         title: {
    //             text: 'Emissions (Mt CO2e)'
    //         },
    //     },xAxis: {
    //     tickPositions: tickposition,
    // },

    //     legend: {
    //         align: 'right',
    //         verticalAlign: 'top',
    //         layout: 'vertical',
    //         x: 10,
    //         y: 250
    //     },

    //     tooltip: {
    //         formatter: function () {
    //             return `<b>Year:</b> ${this.x}<br><b>${this.series.name}:</b>${this.y.toFixed(2)}<br/>`;
    //         }
    //     },

    //     plotOptions: {
    //         column: {
    //             dataLabels: {
    //                 enabled: false
    //             }
    //         }
    //     },

    //     exporting: {
    //         sourceWidth: 1200,
    //         sourceHeight: 600,
    //     }
    // });

    // Chart:GHG_9_2_ag_reduction_source_wide_Mt
    Highcharts.chart("GHG_9_2_ag_reduction_source_wide_Mt", {
      chart: {
        type: "column",
        marginRight: 200,
      },

      title: {
        text: "GHG Emissions Abatement by Non-agricultural Land-use Type",
      },

      credits: {
        enabled: false,
      },

      data: {
        csv: document.getElementById("GHG_9_2_ag_reduction_source_wide_Mt_csv")
          .innerHTML,
      },

      yAxis: {
        title: {
          text: "Greenhouse Gas (Mt CO2e)",
        },
      },
      xAxis: {
        tickPositions: tickposition,
      },

      legend: {
        align: "right",
        verticalAlign: "top",
        layout: "vertical",
        x: 10,
        y: 250,
      },

      tooltip: {
        formatter: function () {
          return `<b>Year:</b> ${this.x}<br><b>${
            this.series.name
          }:</b>${this.y.toFixed(2)}<br/>`;
        },
      },

      plotOptions: {
        column: {
          stacking: "normal",
          dataLabels: {
            enabled: false,
          },
        },
      },

      exporting: {
        sourceWidth: 1200,
        sourceHeight: 600,
      },
    });

    // Chart:GHG_10_GHG_ag_man_df_wide_Mt
    Highcharts.chart("GHG_10_GHG_ag_man_df_wide_Mt", {
      chart: {
        type: "column",
        marginRight: 200,
      },

      title: {
        text: "GHG Emissions Abatement by Agricultural Management Type",
      },

      credits: {
        enabled: false,
      },

      data: {
        csv: document.getElementById("GHG_10_GHG_ag_man_df_wide_Mt_csv")
          .innerHTML,
      },

      yAxis: {
        title: {
          text: "Greenhouse Gas (Mt CO2e)",
        },
      },
      xAxis: {
        tickPositions: tickposition,
      },

      legend: {
        align: "right",
        verticalAlign: "top",
        layout: "vertical",
        x: 10,
        y: 250,
      },

      tooltip: {
        formatter: function () {
          return `<b>Year:</b> ${this.x}<br><b>${
            this.series.name
          }:</b>${this.y.toFixed(2)}<br/>`;
        },
      },

      plotOptions: {
        column: {
          stacking: "normal",
          dataLabels: {
            enabled: false,
          },
        },
      },

      exporting: {
        sourceWidth: 1200,
        sourceHeight: 600,
      },
    });

    // Chart:GHG_11_GHG_ag_man_GHG_crop_lvstk_df_wide_Mt
    Highcharts.chart("GHG_11_GHG_ag_man_GHG_crop_lvstk_df_wide_Mt", {
      chart: {
        type: "column",
        marginRight: 200,
      },

      title: {
        text: "GHG Emissions Abatement by Crop/Livestock",
      },

      credits: {
        enabled: false,
      },

      data: {
        csv: document.getElementById(
          "GHG_11_GHG_ag_man_GHG_crop_lvstk_df_wide_Mt_csv"
        ).innerHTML,
      },

      yAxis: {
        title: {
          text: "Greenhouse Gas (Mt CO2e)",
        },
      },
      xAxis: {
        tickPositions: tickposition,
      },

      legend: {
        align: "right",
        verticalAlign: "top",
        layout: "vertical",
        x: 10,
        y: 250,
      },

      tooltip: {
        formatter: function () {
          return `<b>Year:</b> ${this.x}<br><b>${
            this.series.name
          }:</b>${this.y.toFixed(2)}<br/>`;
        },
      },

      plotOptions: {
        column: {
          stacking: "normal",
          dataLabels: {
            enabled: false,
          },
        },
      },

      exporting: {
        sourceWidth: 1200,
        sourceHeight: 600,
      },
    });

    // Chart:GHG_12_GHG_ag_man_dry_irr_df_wide_Mt
    Highcharts.chart("GHG_12_GHG_ag_man_dry_irr_df_wide_Mt", {
      chart: {
        type: "column",
        marginRight: 200,
      },

      title: {
        text: "GHG Emissions Abatement by Irrigation Type",
      },

      credits: {
        enabled: false,
      },

      data: {
        csv: document.getElementById("GHG_12_GHG_ag_man_dry_irr_df_wide_Mt_csv")
          .innerHTML,
      },

      yAxis: {
        title: {
          text: "Greenhouse Gas (Mt CO2e)",
        },
      },
      xAxis: {
        tickPositions: tickposition,
      },

      legend: {
        align: "right",
        verticalAlign: "top",
        layout: "vertical",
        x: -50,
        y: 250,
      },

      tooltip: {
        formatter: function () {
          return `<b>Year:</b> ${this.x}<br><b>${
            this.series.name
          }:</b>${this.y.toFixed(2)}<br/>`;
        },
      },

      plotOptions: {
        column: {
          stacking: "normal",
          dataLabels: {
            enabled: false,
          },
        },
      },

      exporting: {
        sourceWidth: 1200,
        sourceHeight: 600,
      },
    });
  });
});
