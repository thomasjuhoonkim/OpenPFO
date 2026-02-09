import "react-big-schedule/dist/css/style.css";
import "./Timeline.css";

import { type UseNavigateResult } from "@tanstack/react-router";
import dayjs from "dayjs";
import { Component, type PropsWithChildren } from "react";
import {
  CellUnit,
  DATETIME_FORMAT,
  type EventItem,
  type Resource,
  Scheduler,
  SchedulerData,
  ViewType,
} from "react-big-schedule";
import { DndProvider } from "react-dnd";
import { HTML5Backend } from "react-dnd-html5-backend";

import type { Job, Results } from "@/types/results";

type TimelineProps = PropsWithChildren<{
  results: Results;
  navigate: UseNavigateResult<string>;
}>;
type TimelineState = { viewModel: SchedulerData };

const getJobBgColor = (job: Job) => {
  switch (job.status) {
    case "ready":
      return "#228be6";
    case "running":
      return "#4c6ef5";
    case "failed":
      return "#f03e3e";
    case "complete":
      return "#40c057";
  }
};

export class Timeline extends Component<TimelineProps, TimelineState> {
  constructor(props: TimelineProps) {
    super(props);

    const results = props.results;

    const schedulerData = new SchedulerData(
      dayjs(results.startTime).format(DATETIME_FORMAT),
      ViewType.Custom,
      false,
      false,
      {
        views: [],
        creatable: false,
        movable: false,
        startResizable: false,
        endResizable: false,
        dragAndDropEnabled: false,
        customCellWidth: 10,
        minuteStep: 1,
        headerEnabled: false,
        nonAgendaDayCellHeaderFormat: "MMM D, h:mm A",
        schedulerContentHeight: "100%",
        schedulerWidth: "100%",
        besidesWidth: 0,
        defaultExpanded: false,
        nonWorkingTimeHeadBgColor: "transparent",
        nonWorkingTimeBodyBgColor: "transparent",
        resourceName: "Workflow Item",
      },
      {
        getCustomDateFunc: () => ({
          startDate: dayjs(results.startTime).format(DATETIME_FORMAT),
          endDate: dayjs(results.endTime).format(DATETIME_FORMAT),
          cellUnit: CellUnit.Hour,
        }),
      }
    );

    schedulerData.setResources([
      ...(results.workflow.searches.map((search) => ({
        id: search.id,
        name: search.id,
        // groupOnly: true,
      })) as Resource[]),
      ...(results.workflow.jobs.map((job) => ({
        id: job.id,
        name: job.id,
        parentId: job.searchId,
      })) as Resource[]),
    ]);

    schedulerData.setEvents([
      ...(results.workflow.searches.map((search) => ({
        id: search.id,
        title: search.id,
        resourceId: search.id,
        start: dayjs(search.startTime).format(DATETIME_FORMAT),
        end: dayjs(search.endTime).format(DATETIME_FORMAT),
        bgColor: "#868e96",
        type: "search",
      })) as EventItem[]),
      ...(results.workflow.jobs.map((job) => ({
        id: job.id,
        title: job.id,
        resourceId: job.id,
        groupId: job.searchId,
        start: dayjs(job.startTime).format(DATETIME_FORMAT),
        end: dayjs(job.endTime).format(DATETIME_FORMAT),
        bgColor: getJobBgColor(job),
        type: "job",
      })) as EventItem[]),
    ]);

    this.state = {
      viewModel: schedulerData,
    };
  }

  render() {
    const { viewModel } = this.state;
    return (
      <DndProvider backend={HTML5Backend}>
        <Scheduler
          schedulerData={viewModel}
          prevClick={this.prevClick}
          nextClick={this.nextClick}
          onSelectDate={this.onSelectDate}
          onViewChange={this.onViewChange}
          eventItemClick={this.eventClicked}
          toggleExpandFunc={this.toggleExpandFunc}
        />
      </DndProvider>
    );
  }

  prevClick = () => null;
  nextClick = () => null;
  onViewChange = () => null;
  onSelectDate = () => null;

  eventClicked = (_: any, event: any) => {
    if (event.type === "search") {
      this.props.navigate({
        to: "/results/searches/$searchId",
        params: { searchId: event.id },
      });
    }
    if (event.type === "job") {
      this.props.navigate({
        to: "/results/jobs/$jobId",
        params: { jobId: event.id },
      });
    }
  };

  toggleExpandFunc = (schedulerData: SchedulerData, slotId: string) => {
    schedulerData.toggleExpandStatus(slotId);
    this.setState({ viewModel: schedulerData });
  };
}
