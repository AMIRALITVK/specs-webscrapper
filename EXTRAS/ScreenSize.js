const { spawn } = require("child_process");

var width = 38;
var height = 21;
function inchConverter(size){
    size = size / 2.54;
    return size
}
function screenSize(width, height){
    let pCommand = require("child_process").spawn;
    pCommand("powershell.exe", ["Get-WmiObject -Namespace root\wmi -Class WmiMonitorBasicDisplayParams"]);
    let screen_size = Math.sqrt(Math.pow(inchConverter(width), 2) + Math.pow(inchConverter(height), 2)).toFixed(2);
    return screen_size;
}
console.log(screenSize(width, height));