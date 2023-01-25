import QtQuick 2.15
import QtQuick.Window 2.15
import QtQuick.Layouts 1.2
import QtQuick.Controls 2.15

import "../qml_pages"
import "../qml_components"
import ".."


Item {
    id: createNewFixture
    anchors.fill: parent

    // these properties will get filled and are then passed into python when the user clicks on "create"
    property string fixtureType: "None"
    property string fixtureLibraryId: "None"
    property string fixtureId: "1"
    property string fixtureName: "Fixture X"
    property string fixtureMode: "0"            // For time being, we only support mode 0
    property string fixtureDmxAddress: "0.1"

    Connections {
        target: fixtureLibraryQmlPresentationModel
        function onUpdate_currentFixtureTypeName(name) {
            typeSelectorTextName.text = name
            fixtureType = name
        }
        function onUpdate_currentFixtureTypeId(id) {
            typeSelectorTextId.text = id
            fixtureLibraryId = id
        }
    }
    Rectangle {
        id: background
        anchors.fill: parent
        color: "#1b1b1b"
    }
    Item {
        id: wrapper
        width: 400
        anchors.horizontalCenter: parent.horizontalCenter

        // Fixture Type Selector
        Item {
            id: fixtureTypeSelector
            height: 50
            anchors.top: parent.top
            anchors.topMargin: 10
            Text{
                id: fixtureTypeSelectorText
                text: "Fixture Type:"
                anchors.left: parent.left
                anchors.leftMargin: 10
                anchors.verticalCenter: parent.verticalCenter
                color: "white"
            }
            Rectangle {
                id: fixtureTypeSelectorBackground
                anchors.left: parent.left
                anchors.leftMargin: 100
                width: 300
                height: 50
                color: "white"
                border.color: "black"
                border.width: 1
             
                ComboBox {
                    id: fixtureTypeSelectorComboBox
                    anchors.fill: parent
                    width: 300
                    height: 50
                    model: fixtureLibraryQmlPresentationModel
                    textRole: "display"
                    delegate: delegateTypeSelector
                    background: Rectangle {
                        color: "white"
                        border.color: "black"
                        border.width: 1
                    }
                    onCurrentIndexChanged: {
                        console.log("current index changed to: " + currentIndex)
                        model.update_current_index(currentIndex)
                    }    

                    Rectangle {
                        id: typeSelectorBackground
                        anchors.fill: parent
                        color: "white"
                        border.color: "black"
                        border.width: 1

                        Text {
                            id: typeSelectorTextId
                            anchors.left: parent.left
                            anchors.leftMargin: 10
                            anchors.verticalCenter: parent.verticalCenter
                            text: ""
                            color: "black"
                        }

                        Text {
                            id: typeSelectorTextName
                            anchors.left: typeSelectorTextId.right
                            anchors.leftMargin: 5
                            anchors.verticalCenter: parent.verticalCenter
                            text: "Select a fixture type"
                            color: "black"
                        }
                    }   

                }
            }

        }
        // Delegate component of the type selector ComboBox
        Component {
            id: delegateTypeSelector
            ItemDelegate {
                id: delegateTypeSelectorBackground
                width: 300
                height: 50
                background: Rectangle {
                    color: "white"
                    border.color: "black"
                    border.width: 1
                }
                contentItem: Text {
                    id: text
                    text: model.display.id + " " + model.display.name
                    color: "black"
                }
            }
            
        }

        // Fixture ID Selector
        Item {
            id: fixtureIdSelector
            height: 50
            anchors.top: fixtureTypeSelector.bottom
            anchors.topMargin: 10
            Text{
                id: fixtureIdSelectorText
                text: "Fixture ID:"
                anchors.left: parent.left
                anchors.leftMargin: 10
                anchors.verticalCenter: parent.verticalCenter
                color: "white"
            }

            Rectangle {
                id: fixtureIdSelectorTextInputBackground
                anchors.left: parent.left
                anchors.leftMargin: 100
                width: 300
                height: 50
                color: "white"
                border.color: "black"
                border.width: 1

                TextInput {
                    id: fixtureIdSelectorTextInput
                    anchors.fill: parent
                    width: 300
                    height: 50
                    leftPadding: 10
                    verticalAlignment: TextInput.AlignVCenter
                    color: "black"
                    text: "1"

                    validator: IntValidator {bottom: 1;top: 100000000}

                    onTextChanged: {
                        fixtureId = text
                    }
                }
            } 
        }

        // Fixture Name Selector
        Item {
            id: fixtureNameSelector
            height: 50
            anchors.top: fixtureIdSelector.bottom
            anchors.topMargin: 10
            Text{
                id: fixtureNameSelectorText
                text: "Fixture Name:"
                anchors.left: parent.left
                anchors.leftMargin: 10
                anchors.verticalCenter: parent.verticalCenter
                color: "white"
            }

            Rectangle {
                id: fixtureNameSelectorTextInputBackground
                anchors.left: parent.left
                anchors.leftMargin: 100
                width: 300
                height: 50
                color: "white"
                border.color: "black"
                border.width: 1

                TextInput {
                    id: fixtureNameSelectorTextInput
                    anchors.fill: parent
                    width: 300
                    height: 50
                    leftPadding: 10
                    verticalAlignment: TextInput.AlignVCenter
                    color: "black"
                    text: "Fixture X"

                    onTextChanged: {
                        fixtureName = text
                    }
                }
            }
        }

        // Fixture Dmx Address Selector
        Item {
            id: fixtureDmxAddressSelector
            anchors.top: fixtureNameSelector.bottom
            anchors.topMargin: 10
            height: 50

            Text{
                id: fixtureDmxAddressSelectorText
                text: "DMX Address:"
                anchors.left: parent.left
                anchors.leftMargin: 10
                anchors.verticalCenter: parent.verticalCenter
                color: "white"
            }

            Rectangle {
                id: fixtureDmxAddressSelectorTextInputBackground
                anchors.left: parent.left
                anchors.leftMargin: 100
                width: 300
                height: 50
                color: "white"
                border.color: "black"
                border.width: 1

                TextInput {
                    id: fixtureDmxAddressSelectorTextInput
                    anchors.fill: parent
                    width: 300
                    height: 50
                    leftPadding: 10
                    verticalAlignment: TextInput.AlignVCenter
                    color: "black"
                    text: "0.1"

                    onTextChanged: {
                        fixtureDmxAddress = text
                    }
                }
            }
        }

        // Submit Button
        Item {
            id: submitButton
            anchors.top: fixtureDmxAddressSelector.bottom
            anchors.topMargin: 15
            anchors.horizontalCenter: parent.horizontalCenter
            
            Button {
                id: submitButtonButton
                width: 400
                height: 50
                z: 2
                anchors.horizontalCenter: parent.horizontalCenter
                text: "Create"
                background: Rectangle {
                    color: "green"
                    border.color: "black"
                    border.width: 1
                }
                onClicked: {
                    console.log("submit button clicked")
                    dmxFixturePatchQmlPresentationModel.add_fixture(fixtureType, fixtureLibraryId, fixtureId, fixtureName, fixtureMode, fixtureDmxAddress)
                }

            }
        }
    }
    
}
