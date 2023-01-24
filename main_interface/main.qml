import QtQuick 2.5
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.2

ApplicationWindow {
    id: root
    visible: true
    width: 1920
    height: 1080
    title: "Hello World"
    property string value: "1"
    property QtObject backend
    visibility: "FullScreen"

    // BACKGROUND
    Rectangle {
        id: main_background
        anchors.fill: parent

        Image {
            anchors.fill: parent
            source: "./images/Background.png"
            fillMode: Image.PreserveAspectCrop
        }
    }
    


    Test {
        id: test
    }



    // GRID SNAP SYSTEM X
    property bool placeHolderVisibility: false

    property int in_which_snap_line: null
    property variant snap_lines_x:  [185, 185 + 91, 185 + 91 * 2, 185 + 91 * 3, 185 + 91 * 4, 185 + 91 * 5, 185 + 91 * 6, 185 + 91 * 7, 185 + 91 * 8, 185 + 91 * 9, 185 + 91 * 10, 185 + 91 * 11, 185 + 91 * 12, 185 + 91 * 13, 185 + 91 * 14, 185 + 91 * 15, 185 + 91 * 16, 185 + 91 * 17, 185 + 91 * 18]

    

    Rectangle {
        id: dragableWindow
        width: 80
        height: 80
        color: "white"
        Drag.active: dragArea.drag.active
        opacity: 1
        z: 2

        Component.onCompleted: update()  // as soon as the component is created, update the label
        onXChanged: 
        {
            placeHolderVisibility = true
            for (var i = 0; i < 18; i++) {
                if (dragableWindow.x >= snap_lines_x[i] && dragableWindow.x <= snap_lines_x[i] + 91 / 2  || dragableWindow.x >= snap_lines_x[i] - 91 / 2 && dragableWindow.x <= snap_lines_x[i]) {
                    in_which_snap_line = i
                }
            }
        }

        MouseArea {
            id: dragArea
            anchors.fill: parent
            drag {
                target: parent
                axis: "XAxis"
                minimumX: 0
                maximumX: 1920 - width

            }

            onReleased: {
                placeHolderVisibility = false
                dragableWindow.x = placeHolderRect.x
            }
            
        }
    }

    Rectangle {
        id: placeHolderRect
        color: "orange"
        width: dragableWindow.width
        height: dragableWindow.height
        opacity: 0.3
        z: 1
        visible: placeHolderVisibility
        x: root.snap_lines_x[root.in_which_snap_line]
    }

    
    // GRID CROSS DISPLAY
    GridLayout {
        columns: 18
        rows: 10
        anchors.topMargin: 25
        anchors.leftMargin: 141
        anchors.rightMargin: 141
        anchors.bottomMargin: 155
        anchors.fill: parent
        // columnSpacing: 150

        Cross {Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter}
        Cross {Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter}
        Cross {Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter}
        Cross {Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter}
        Cross {Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter}
        Cross {Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter}
        Cross {Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter}
        Cross {Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter}
        Cross {Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter}
        Cross {Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter}
        Cross {Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter}
        Cross {Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter}
        Cross {Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter}
        Cross {Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter}
        Cross {Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter}
        Cross {Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter}
        Cross {Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter}
        Cross {Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter}
        Cross {Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter}
        Cross {Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter}
        Cross {Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter}
        Cross {Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter}
        Cross {Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter}
        Cross {Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter}
        Cross {Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter}
        Cross {Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter}
        Cross {Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter}
        Cross {Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter}
        Cross {Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter}
        Cross {Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter}
        Cross {Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter}
        Cross {Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter}
        Cross {Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter}
        Cross {Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter}
        Cross {Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter}
        Cross {Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter}
        Cross {Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter}
        Cross {Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter}
        Cross {Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter}
        Cross {Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter}
        Cross {Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter}
        Cross {Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter}
        Cross {Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter}
        Cross {Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter}
        Cross {Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter}
        Cross {Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter}
        Cross {Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter}
        Cross {Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter}
        Cross {Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter}
        Cross {Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter}
        Cross {Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter}
        Cross {Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter}
        Cross {Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter}
        Cross {Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter}
        Cross {Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter}
        Cross {Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter}
        Cross {Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter}
        Cross {Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter}
        Cross {Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter}
        Cross {Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter}
        Cross {Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter}
        Cross {Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter}
        Cross {Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter}
        Cross {Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter}
        Cross {Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter}
        Cross {Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter}
        Cross {Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter}
        Cross {Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter}
        Cross {Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter}
        Cross {Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter}
        Cross {Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter}
        Cross {Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter}
        Cross {Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter}
        Cross {Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter}
        Cross {Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter}
        Cross {Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter}
        Cross {Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter}
        Cross {Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter}
        Cross {Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter}
        Cross {Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter}
        Cross {Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter}
        Cross {Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter}
        Cross {Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter}
        Cross {Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter}
        Cross {Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter}
        Cross {Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter}
        Cross {Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter}
        Cross {Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter}
        Cross {Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter}
        Cross {Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter}
        Cross {Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter}
        Cross {Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter}
        Cross {Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter}
        Cross {Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter}
        Cross {Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter}
        Cross {Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter}
        Cross {Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter}
        Cross {Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter}
        Cross {Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter}
        Cross {Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter}
        Cross {Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter}
        Cross {Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter}
        Cross {Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter}
        Cross {Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter}
        Cross {Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter}
        Cross {Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter}
        Cross {Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter}
        Cross {Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter}
        Cross {Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter}
        Cross {Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter}
        Cross {Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter}
        Cross {Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter}
        Cross {Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter}
        Cross {Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter}
        Cross {Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter}
        Cross {Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter}
        Cross {Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter}
        Cross {Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter}
        Cross {Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter}
        Cross {Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter}
        Cross {Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter}
        Cross {Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter}
        Cross {Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter}
        Cross {Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter}
        Cross {Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter}
        Cross {Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter}
        Cross {Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter}
        Cross {Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter}
        Cross {Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter}
        Cross {Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter}
        Cross {Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter}
        Cross {Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter}
        Cross {Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter}
        Cross {Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter}
        Cross {Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter}
        Cross {Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter}
        Cross {Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter}
        Cross {Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter}
        Cross {Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter}
        Cross {Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter}
        Cross {Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter}
        Cross {Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter}
        Cross {Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter}
        Cross {Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter}
        Cross {Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter}
        Cross {Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter}
        Cross {Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter}
        Cross {Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter}
        Cross {Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter}
        Cross {Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter}
        Cross {Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter}
        Cross {Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter}
        Cross {Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter}
        Cross {Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter}
        Cross {Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter}
        Cross {Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter}
        Cross {Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter}
        Cross {Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter}
        Cross {Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter}
        Cross {Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter}
        Cross {Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter}
        Cross {Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter}
        Cross {Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter}
        Cross {Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter}
        Cross {Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter}
        Cross {Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter}
        Cross {Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter}
        Cross {Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter}
        Cross {Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter}
        Cross {Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter}
        Cross {Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter}
        Cross {Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter}
        Cross {Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter}
        Cross {Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter}
        Cross {Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter}
        Cross {Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter}
        Cross {Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter}
        Cross {Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter}
        Cross {Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter}
        Cross {Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter}
        
    }

}
