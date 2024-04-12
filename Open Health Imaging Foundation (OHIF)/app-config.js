window.config = {
  routerBasename: "/",
  extensions: [],
  modes: [],
  showStudyList: true,
  dataSources: [
    {
      namespace: "@ohif/extension-default.dataSourcesModule.dicomweb",
      sourceName: "dicomweb",
      configuration: {
        friendlyName: "dcmjs DICOMWeb Server",
        name: "DCM4CHEE",
        wadoUriRoot: "https://server.dcmjs.org/dcm4chee-arc/aets/DCM4CHEE/wado",
        qidoRoot: "https://server.dcmjs.org/dcm4chee-arc/aets/DCM4CHEE/rs",
        wadoRoot: "https://server.dcmjs.org/dcm4chee-arc/aets/DCM4CHEE/rs",
        qidoSupportsIncludeField: true,
        supportsReject: true,
        imageRendering: "wadors",
        thumbnailRendering: "wadors",
        enableStudyLazyLoad: true,
        supportsFuzzyMatching: true,
        supportsWildcard: true,
        omitQuotationForMultipartRequest: true,
      },
    },
  ],
  defaultDataSourceName: "dicomweb",
};
