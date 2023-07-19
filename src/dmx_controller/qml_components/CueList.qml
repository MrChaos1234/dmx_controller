import QtQuick 2.15
import QtQuick.Window 2.15
import QtQuick.Layouts 1.2
import QtQuick.Controls 2.15

import "../qml_pages"
import "../qml_components"
import ".."

Item {
    id: cueList
    width: 650
    
    property bool show_only: false

    Rectangle {
        id: cueListBackground
        anchors.fill: parent
        color: "black"
    }

    anchors {
        left: parent.left
        top: parent.top
        bottom: parent.bottom
    }

    // Header
    Rectangle {
        id: cueListHeader
        anchors {
            left: parent.left
            top: parent.top
            right: parent.right
        }
        height: 50
        color: "orange"
        Text {
            id: cueListHeaderText
            anchors.verticalCenter: parent.verticalCenter
            anchors.horizontalCenter: parent.horizontalCenter
            text: "Cue List"
            font.family: "TW Cen MT"
            font.pixelSize: 23
            font.styleName: "Bold"
            color: "black"
        }
    }


    // Description
    Rectangle {
        id: cueListDescription
        anchors {
            left: parent.left
            top: cueListHeader.bottom
            right: parent.right
        }
        height: 50
        color: "black"

        Rectangle {
            id: cueListDescriptionSelectBox
            height: 50
            width: 50
            anchors.top: parent.top
            anchors.left: parent.left
            anchors.leftMargin: 4
            color: "#2a2a2a"
        }

        Rectangle {
            id: cueListDescriptionIdBox
            anchors.left: cueListDescriptionSelectBox.right
            anchors.leftMargin: 4
            height: 50
            width: 96
            color: "#2a2a2a"

            Text {
                id: cueListDescriptionId
                anchors.centerIn: parent
                text: "ID"
                font.family: "TW Cen MT"
                font.pixelSize: 22
                color: "white"
            }
        }
        
        Rectangle {
            id: cueListDescriptionNameBox
            anchors.left: cueListDescriptionIdBox.right
            anchors.leftMargin: 4
            height: 50
            width: 300
            color: "#2a2a2a"

            Text {
                id: cueListDescriptionName
                anchors.centerIn: parent
                text: "NAME"
                font.family: "TW Cen MT"
                font.pixelSize: 22
                color: "white"
            }
        }

        Rectangle {
            id: cueListDescriptionGroupBox
            anchors.left: cueListDescriptionNameBox.right
            anchors.leftMargin: 4
            height: 50
            width: 50
            color: "#2a2a2a"

            Text {
                id: cueListDescriptionGroup
                anchors.centerIn: parent
                text: "GROUP"
                font.family: "TW Cen MT"
                font.pixelSize: 12
                color: "white"
            }
        }

        Rectangle {
            id: cueListDescriptionDmxDataBox
            anchors.left: cueListDescriptionGroupBox.right
            anchors.leftMargin: 4
            height: 50
            width: 130
            color: "#2a2a2a"

            Text {
                id: cueListDescriptionDmxData
                anchors.centerIn: parent
                text: "DATA"
                font.family: "TW Cen MT"
                font.pixelSize: 22
                color: "white"
            }
        }
    }


    // List
    Component {
        id: delegate
        Rectangle {
            id: wrapper
            height: 40
            color: "black"
            Rectangle {
                id: listElementSelectBox
                height: 40
                width: 50
                anchors.top: parent.top
                anchors.left: parent.left
                anchors.leftMargin: 4
                color: "#2a2a2a"
                Rectangle {
                    id: listElementSelect
                    anchors.centerIn: parent
                    width: 30
                    height: 30
                    color: display.selected ? "orange" : "white"
                }
                MouseArea {
                    anchors.fill: parent
                    onClicked: {
                        cueListQmlPresentationModel.select(index)
                    }                        
                } 
                //display.selected
            }

            Rectangle {
                id: listElementIdBox
                anchors.left: listElementSelectBox.right
                anchors.leftMargin: 4
                height: 40
                width: 96
                color: "#2a2a2a"
                Text {
                    id: listElementId
                    anchors.centerIn: parent
                    text: display.identifier
                    font.family: "TW Cen MT"
                    font.pixelSize: 17
                    color: "white"
                }
            }
            Rectangle {
                id: listElementTypeBox
                anchors.left: listElementIdBox.right
                anchors.leftMargin: 4
                height: 40
                width: 300
                color: "#2a2a2a"
                Text {
                    id: listElementType
                    anchors.centerIn: parent
                    text: display.cue_name
                    font.family: "TW Cen MT"
                    font.pixelSize: 17
                    color: "white"
                }
            }
            Rectangle {
                id: listElementNameBox
                anchors.left: listElementTypeBox.right
                anchors.leftMargin: 4
                height: 40
                width: 50
                color: "#2a2a2a"
                Text {
                    id: listElementName
                    anchors.centerIn: parent
                    text: display.cue_group
                    font.family: "TW Cen MT"
                    font.pixelSize: 17
                    color: "white"
                }
            }
            Rectangle {
                id: listElementDmxBox
                anchors.left: listElementNameBox.right
                anchors.leftMargin: 4
                height: 40
                width: 130
                color: "#2a2a2a"
                Text {
                    id: listElementDmx
                    anchors.centerIn: parent
                    text: "exists"
                    font.family: "TW Cen MT"
                    font.pixelSize: 17
                    color: "white"
                }
            }               
        }
    }

    ListView {
        id: listView
        cacheBuffer: 100
        reuseItems: true
        anchors {
            left: parent.left
            top: cueListDescription.bottom
            right: parent.right
            bottom: cueListFooter.top
            topMargin: 4
        }
        model: cueListQmlPresentationModel
        clip: true
        focus: true
        spacing: 4
        delegate: delegate
        property int dragItemIndex: -1

    }

    // Footer with buttons
    Rectangle {
        id: cueListFooter
        anchors {
            left: parent.left
            right: parent.right
            bottom: parent.bottom
        }
        color: "orange"
        height: 50
        width: parent.width

        GridLayout {
            anchors.fill: parent
            height: 50
            width: parent.width
            columns: 1
            visible: !show_only

            Rectangle {
                id: cueListFooterRemoveButton
                Layout.alignment: Qt.AlignCenter
                height: 42
                width: 42
                color: "red"
                Layout.column: 0
                border.color: "black"
                border.width: 2

                Image {
                    id: cueListFooterRemoveButtonImage
                    anchors.centerIn: parent
                    width: 30
                    height: 30
                    source: "../res/trash_can.png"
                }

                MouseArea {
                    anchors.fill: parent
                    onClicked: {
                        cueListQmlPresentationModel.remove_selected_cues()
                    }
                }
            }
        }
    }
    

}