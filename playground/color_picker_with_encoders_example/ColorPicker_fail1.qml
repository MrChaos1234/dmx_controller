import QtQuick 2.5
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.2
import QtQuick.Window 2.15
import QtGraphicalEffects 1.12

Item {
    id: root
    property int pos_x: 0
    property int pos_y: 0
    property string choosen_color: ""

    property real h: 0
    property real s: 0
    property real v: 0

    property real r: 0
    property real g: 0
    property real b: 0
    property real i: 0
    property real f: 0
    property real p: 0
    property real q: 0
    property real t: 0

    property real a: 0

    property string rbga: "'#000000'"


    Rectangle {
        id: color_picker
        anchors.centerIn: parent
        width: 480
        height: 480
        color: white

        Canvas {
            id: canvas
            anchors.fill: parent
            onPaint: {
                var ctx = getContext("2d");
                ctx.lineWidth = 1;
                for (var row = 0; row < 480; row++) {
                    for (var collumn = 0; collumn < 240; collumn++) {
                        pos_x = 0 + collumn
                        pos_y = 240 - row

                        if (pos_x > 0 && pos_y > 0) {
                            choosen_color = 90 - Math.abs((Math.atan(pos_y / pos_x)) * (180 / Math.PI))
                        }
                        if (pos_x > 0 && pos_y < 0) {
                            choosen_color = Math.abs((Math.atan(pos_y / pos_x)) * (180 / Math.PI)) + 90
                        }
                        if (pos_x < 0 && pos_y < 0) {
                            choosen_color = 90 - Math.abs((Math.atan(pos_y / pos_x)) * (180 / Math.PI)) + 180
                        }
                        if (pos_x < 0 && pos_y > 0) {
                            choosen_color = Math.abs((Math.atan(pos_y / pos_x)) * (180 / Math.PI)) + 270
                        }
                        
                        // calculate saturation with distance
                        s = (Math.sqrt(Math.pow(pos_x, 2) + Math.pow(pos_y, 2))) / 240
                    
                        // value is always 1
                        v = 1

                        // convert hsv to rgb
                        h = choosen_color / 360
                        s = s
                        v = v                
                        i = Math.floor(h * 6);
                        f = h * 6 - i;
                        p = v * (1 - s);
                        q = v * (1 - f * s);
                        t = v * (1 - (1 - f) * s);
                        switch (i % 6) {
                            case 0: r = v, g = t, b = p; break;
                            case 1: r = q, g = v, b = p; break;
                            case 2: r = p, g = v, b = t; break;
                            case 3: r = p, g = q, b = v; break;
                            case 4: r = t, g = p, b = v; break;
                            case 5: r = v, g = p, b = q; break;
                        }
                        r = Math.round(r * 255)
                        g = Math.round(g * 255)
                        b = Math.round(b * 255)

                        // convert rgb to hex            
                        rbga = "#" + r.toString(16).padStart(2, "0") + g.toString(16).padStart(2, "0") + b.toString(16).padStart(2, "0")

                        ctx.strokeStyle = rbga
                        ctx.beginPath();
                        ctx.moveTo(240 + collumn, 0 + row);
                        ctx.lineTo(241 + collumn, 1 + row);
                        ctx.stroke();

                        console.log((a / (480*240)) * 100 + "% => " + pos_x + " " + pos_y + " " + " " + h + " " + s + " " + v + " " + rbga)
                        a = a + 1
                    }
                }                
            }
        }


        MouseArea {
            anchors.fill: parent
            onClicked: {
                // calculate hue with angle
                pos_x = mouse.x - 240
                pos_y = 0 - (mouse.y - 240)

                if (pos_x > 0 && pos_y > 0) {
                    choosen_color = 90 - Math.abs((Math.atan(pos_y / pos_x)) * (180 / Math.PI))
                }
                if (pos_x > 0 && pos_y < 0) {
                    choosen_color = Math.abs((Math.atan(pos_y / pos_x)) * (180 / Math.PI)) + 90
                }
                if (pos_x < 0 && pos_y < 0) {
                    choosen_color = 90 - Math.abs((Math.atan(pos_y / pos_x)) * (180 / Math.PI)) + 180
                }
                if (pos_x < 0 && pos_y > 0) {
                    choosen_color = Math.abs((Math.atan(pos_y / pos_x)) * (180 / Math.PI)) + 270
                }
                
                // calculate saturation with distance
                s = (Math.sqrt(Math.pow(pos_x, 2) + Math.pow(pos_y, 2))) / 240
             
                // value is always 1
                v = 1

                // convert hsv to rgb
                h = choosen_color / 360
                s = s
                v = v                
                i = Math.floor(h * 6);
                f = h * 6 - i;
                p = v * (1 - s);
                q = v * (1 - f * s);
                t = v * (1 - (1 - f) * s);
                switch (i % 6) {
                    case 0: r = v, g = t, b = p; break;
                    case 1: r = q, g = v, b = p; break;
                    case 2: r = p, g = v, b = t; break;
                    case 3: r = p, g = q, b = v; break;
                    case 4: r = t, g = p, b = v; break;
                    case 5: r = v, g = p, b = q; break;
                }
                r = Math.round(r * 255)
                g = Math.round(g * 255)
                b = Math.round(b * 255)

                // convert rgb to hex            
                rbga = "#" + r.toString(16).padStart(2, "0") + g.toString(16).padStart(2, "0") + b.toString(16).padStart(2, "0")
                console.log(rbga)
            }
        }
    }

    Text {
        id: debug_text
        anchors.top: parent.bottom
        text: pos_x + " x " + pos_y + " " + r + " " + g + " " + b
    }
} 

