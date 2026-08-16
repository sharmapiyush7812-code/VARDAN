/**
 * VARDAN — Apps Script Web App entry point
 * Deploy: Extensions > Apps Script > Deploy > New deployment > Web app
 */

function doGet() {
  return HtmlService.createHtmlOutputFromFile('Index')
    .setTitle('VARDAN — Built Different')
    .addMetaTag('viewport', 'width=device-width, initial-scale=1.0, viewport-fit=cover')
    .setXFrameOptionsMode(HtmlService.XFrameOptionsMode.ALLOWALL);
}