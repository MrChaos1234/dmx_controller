import QtQuick 2.15
import QtQuick.Window 2.15
import QtQuick.Layouts 1.2
import QtQuick.Controls 2.15

import "../qml_pages"
import "../qml_components"
import ".."

Item {
    id: dmxList
   
    Rectangle {
        id: fixturePatchBackground
        anchors.fill: parent
        color: "#121212"
        border.color: "orange"
        border.width: 2
    }

    GridView {
        id: listView
        anchors.fill: parent
        anchors.topMargin: 4
        anchors.leftMargin: 10
        model: dmxListQmlPresentationModel
        delegate: delegate
        cellWidth: 26.5
        cellHeight: 14

    }

    Component {
        id: delegate

        Rectangle {
            id: wrapper

            Text {
                id: listElementId
                text: display.channel_id
                font.family: "TW Cen MT"
                font.pixelSize: 10
                color: "white"
            }

            Rectangle {
                id: h
                color: "orange"
                visible: {
                    if(display.fixture_id != "empty") 
                        visible = true
                    else
                        visible = false
                }
                
            }
        }
    
        
    }

    
    // List
    // Component {
    //     id: delegate
    //     Rectangle {
    //         id: wrapper
    //         height: 50
    //         color: "black"
    //         Rectangle {
    //             id: listElementSelectBox
    //             height: 50
    //             width: 50
    //             anchors.top: parent.top
    //             anchors.left: parent.left
    //             anchors.leftMargin: 4
    //             color: "#2a2a2a"
    //             Rectangle {
    //                 id: listElementSelect
    //                 anchors.centerIn: parent
    //                 width: 30
    //                 height: 30
    //                 color: display.selected ? "orange" : "white"
    //             }
    //             MouseArea {
    //                 anchors.fill: parent
    //                 onClicked: {
    //                     dmxFixturePatchQmlPresentationModel.select(index)
    //                 }                        
    //             } 
    //             //display.selected
    //         }
    //         Rectangle {
    //             id: listElementIdBox
    //             anchors.left: listElementSelectBox.right
    //             anchors.leftMargin: 4
    //             height: 50
    //             width: 96
    //             color: "#2a2a2a"
    //             Text {
    //                 id: listElementId
    //                 anchors.centerIn: parent
    //                 text: display.identifier
    //                 font.family: "TW Cen MT"
    //                 font.pixelSize: 22
    //                 color: "white"
    //             }
    //         }
    //         Rectangle {
    //             id: listElementTypeBox
    //             anchors.left: listElementIdBox.right
    //             anchors.leftMargin: 4
    //             height: 50
    //             width: 150
    //             color: "#2a2a2a"
    //             Text {
    //                 id: listElementType
    //                 anchors.centerIn: parent
    //                 text: display.fixture_name
    //                 font.family: "TW Cen MT"
    //                 font.pixelSize: 22
    //                 color: "white"
    //             }
    //         }
    //         Rectangle {
    //             id: listElementNameBox
    //             anchors.left: listElementTypeBox.right
    //             anchors.leftMargin: 4
    //             height: 50
    //             width: 200
    //             color: "#2a2a2a"
    //             Text {
    //                 id: listElementName
    //                 anchors.centerIn: parent
    //                 text: display.fixture_display_name
    //                 font.family: "TW Cen MT"
    //                 font.pixelSize: 22
    //                 color: "white"
    //             }
    //         }
    //         Rectangle {
    //             id: listElementDmxBox
    //             anchors.left: listElementNameBox.right
    //             anchors.leftMargin: 4
    //             height: 50
    //             width: 80
    //             color: "#2a2a2a"
    //             Text {
    //                 id: listElementDmx
    //                 anchors.centerIn: parent
    //                 text: display.dmx_start_address
    //                 font.family: "TW Cen MT"
    //                 font.pixelSize: 22
    //                 color: "white"
    //             }
    //         }
    //     }
    // }

    // ListView {
    //     id: listView
    //     cacheBuffer: 100
    //     reuseItems: true
    //     anchors {
    //         left: parent.left
    //         top: fixturePatchDescription.bottom
    //         right: parent.right
    //         bottom: parent.bottom
    //         topMargin: 4
    //     }
    //     model: dmxFixturePatchQmlPresentationModel
    //     clip: true
    //     focus: true
    //     spacing: 4
    //     delegate: delegate

    // }   

}