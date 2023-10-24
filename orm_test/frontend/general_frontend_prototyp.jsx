<GeneralFrontendAsset
  name="MyAsset"
  api_data={{
    data: "/api/project",
    project_type: "/api/reference/project_type",
  }}
  view_list={["detail_addon"]}
  size_list={["1x1", "1x2", "1x3"]}
  filter_list={[
    {
      view: "list",
      jsx: (
        <YearSlider
          filter={{ keyword: "year", url: "/api/project" }}
          start_year={2023}
          end_year={2024}
          max_year={2030}
          min_year={2020}
        ></YearSlider>
      ),
    },
  ]}
  element_list={[
    {
      view: "detail",
      jsx: (
        <div>
          <input link_to_data={data.value123}></input>
          <dropdown
            value_list={project_type}
            link_to_data={data.project_type}
          ></dropdown>
        </div>
      ),
      key: "project_type",
      help_txt: "I am here to assign project type ...",
      help_url: "https://www.docu.com/MyAsset/ProjectType",
    },
    {
      view: "list",
      jsx: (
        <table
          link_to_data={data}
          key_list={{
            1: ["s"],
            2: ["s", "m"],
          }}
          link={{
            callback: (element) => changeView("detail", element.id),
            cursor: () => "showDetail",
          }}
          scroll_y={button_scroll1}
          scroll_x={button_scroll2}
        ></table>
      ),
      key: "project_table",
    },
  ]}
  button_dict={{
    save123: {
      handleClick: () => {
        console.log("save");
      },
      text: "Save",
      disabled: false,
      view_list: ["detail"],
    },
  }}
  checker_list={[
    {
      value_checker: (value) => {
        data.project_type > data.value123;
      },
      check_time: "onchange",
      comment: "project_type must be greater than value123",
    },
  ]}
  view_config={[
    { key: "project_table", size: "1x1", position: "5/7" },
    { key: "project_type", size: "1x1", position: "1/1" },
  ]}
/>;

function GeneralFrontendAsset({
  name,
  api_data,
  view_list,
  size_list,
  filter_list,
  element_list,
  button_dict,
  checker_list,
  view_config,
}) {}
