# Tai Sakuma <tai.sakuma@gmail.com>

from .splitfuncs import create_file_start_length_list

##__________________________________________________________________||
class DatasetIntoEventBuildersSplitter(object):

    def __init__(self, EventBuilder, eventBuilderConfigMaker,
                 maxEvents=-1, maxEventsPerRun=-1,
                 maxFiles=-1, maxFilesPerRun=1
    ):

        self.EventBuilder = EventBuilder
        self.eventBuilderConfigMaker = eventBuilderConfigMaker
        self.maxEvents = maxEvents
        self.maxEventsPerRun = maxEventsPerRun
        self.maxFiles = maxFiles
        self.maxFilesPerRun = maxFilesPerRun
        self.create_file_start_length_list = create_file_start_length_list

    def __repr__(self):
        return '{}(EventBuilder={!r}, eventBuilderConfigMaker={!r}, maxEvents={!r}, maxEventsPerRun={!r}, maxFiles={!r}, maxFilesPerRun={!r})'.format(
            self.__class__.__name__,
            self.EventBuilder,
            self.eventBuilderConfigMaker,
            self.maxEvents,
            self.maxEventsPerRun,
            self.maxFiles,
            self.maxFilesPerRun
        )

    def __call__(self, dataset):

        files = self.eventBuilderConfigMaker.file_list_in(dataset, maxFiles=self.maxFiles)
        # e.g., ['A.root', 'B.root', 'C.root', 'D.root', 'E.root']

        file_start_length_list = self._file_start_length_list(
            files,
            maxEvents=self.maxEvents,
            maxEventsPerRun=self.maxEventsPerRun,
            maxFilesPerRun=self.maxFilesPerRun
        )
        # (files, start, length)
        # e.g.,
        # [
        #     (['A.root'], 0, 80),
        #     (['A.root', 'B.root'], 80, 80),
        #     (['B.root'], 60, 80),
        #     (['B.root', 'C.root'], 140, 80),
        #     (['C.root'], 20, 10)
        # ]

        configs = self._create_configs(dataset, file_start_length_list)
        eventBuilders = [self.EventBuilder(c) for c in configs]
        return eventBuilders

    def _file_start_length_list(self, files, maxEvents=-1, maxEventsPerRun=-1,
                                maxFilesPerRun=1):

        if not self._need_get_number_of_events_in_files(maxEvents, maxEventsPerRun):
            return self._fast_path(files, maxFilesPerRun)

        return self._full_path(files, maxEvents, maxEventsPerRun, maxFilesPerRun)

    def _need_get_number_of_events_in_files(self, maxEvents, maxEventsPerRun):
        return maxEvents >= 0 or maxEventsPerRun >= 0

    def _fast_path(self, files, maxFilesPerRun):
        if not files:
            return [ ]
        if maxFilesPerRun < 0:
            return [(files, 0, -1)]
        if maxFilesPerRun == 0:
            return [ ]
        return [(files[i:(i + maxFilesPerRun)], 0, -1) for i in range(0, len(files), maxFilesPerRun)]

    def _full_path(self, files, maxEvents, maxEventsPerRun, maxFilesPerRun):

        # this can be slow
        file_nevents_list = self._file_nevents_list_(
            files,
            maxEvents=maxEvents
        )

        file_start_length_list = self.create_file_start_length_list(
            file_nevents_list=file_nevents_list,
            max_events_per_run=maxEventsPerRun,
            max_events_total=maxEvents,
            max_files_per_run=maxFilesPerRun
        )
        return file_start_length_list

    def _file_nevents_list_(self, files, maxEvents=-1):
        totalEvents = 0
        ret = [ ]
        for f in files:
            if 0 <= maxEvents <= totalEvents:
                break

            # this can be slow
            n = self.eventBuilderConfigMaker.nevents_in_file(f)

            ret.append((f, n))
            totalEvents += n
        return ret

    def _create_configs(self, dataset, file_start_length_list):
        configs = [ ]
        for files, start, length in file_start_length_list:
            config = self.eventBuilderConfigMaker.create_config_for(dataset, files, start, length)
            configs.append(config)
        return configs
##__________________________________________________________________||
