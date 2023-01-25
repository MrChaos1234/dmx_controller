import QtQuick 2.5
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.2
import QtQuick.Window 2.15


Item {
    id: root

    property int r: 0
    property int g: 0
    property int b: 0
    property int a: 0

    property string darker_color: "#1b1b1b"



    // property color set_color: Qt.rgba(r, g, b, a/100)

    property string set_color: "#" + a.toString(16).padStart(2, "0") + r.toString(16).padStart(2, "0") + g.toString(16).padStart(2, "0") + b.toString(16).padStart(2, "0")


    Rectangle {
        anchors.centerIn: parent
        width: 480
        height: 270
        color: darker_color

        Rectangle {
            id: color_display
            anchors.top: parent.top
            anchors.topMargin: 10
            anchors.horizontalCenter: parent.horizontalCenter
            width: parent.width - 20
            height: 100
            color: set_color
        }
    }

}