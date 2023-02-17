"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
const express_1 = __importDefault(require("express"));
const path_1 = __importDefault(require("path"));
const pong_1 = require("./pong");
////////////////////////////// Setup ///////////////////////////////////////////
const HOST_NAME = 'splines.portal';
const FRONTEND_FOLDER = path_1.default.join(__dirname, '../', 'public');
const app = (0, express_1.default)();
// Redirect every request to our application
// https://raspberrypi.stackexchange.com/a/100118
// [You need a self-signed certificate if you really want 
// an https connection. In my experience, this is just a pain to do
// and probably overkill for a project where you have your own WiFi network
// without Internet access anyway.]
app.use((req, res, next) => {
    if (req.hostname != HOST_NAME) {
        return res.redirect(`http://${HOST_NAME}`);
    }
    next();
});
// Call this AFTER app.use where we do the redirects
app.use(express_1.default.static(FRONTEND_FOLDER));
/////////////////////////////// Endpoints //////////////////////////////////////
// Serve frontend
app.get('/', (req, res, next) => {
    res.sendFile(path_1.default.join(FRONTEND_FOLDER, 'index.html'));
});
app.get('/api/ping', pong_1.pong);
///////////////////////////// Server listening /////////////////////////////////
// Listen for requests
// If you change the port here, you have to adjust the ip tables as well
// see file: access-point/setup-access-point.sh
const PORT = 3000;
app.listen(PORT, () => {
    console.log(`Node version: ${process.version}`);
    console.log(`⚡ Raspberry Pi Server listening on port ${PORT}`);
});
