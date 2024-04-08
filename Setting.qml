import QtQuick 6.5
import QtQuick.Controls 6.5
import QtQuick.Controls.Fusion
import QtQuick.Layouts


Item {
    id: config


    function load(){
        let l = base.get_config()
        config_login.text = l[0]
        config_pass.text = l[1]
        config_token.text = l[2]
        config_token_np.text = l[3]
    }

    QtObject {
        id: internal

        function get_token(){
            var l = []
            l[0] = config_login.text
            l[1] = config_pass.text

            // config_token.text = xls.get_token(l)
            config_token.text = api_checkbox.get_token(l)
        }

        function set_config(){
            var l = []
            l[0] = config_login.text
            l[1] = config_pass.text
            l[2] = config_token.text
            l[3] = config_token_np.text

            var r = base.set_config(l)

            console.info(r[0])
        }


    }



    ColumnLayout {
        anchors.fill: parent
        anchors.leftMargin: 20
        anchors.rightMargin: 20
        anchors.topMargin: 20
        anchors.bottomMargin: 20
        spacing: 15

        Label {
            Layout.fillWidth: true
            Layout.leftMargin: 20
            Layout.minimumHeight: 40
            Layout.maximumHeight: 40
            font.pointSize: 13
            text: qsTr("Касир")
            verticalAlignment: Qt.AlignVCenter
        }

        RowLayout {
            Layout.fillWidth: true
            Layout.minimumHeight: 30
            Layout.maximumHeight: 30
            spacing: 15

            Item {
                Layout.fillWidth: true
            }

            Label {
                Layout.fillHeight: true
                Layout.minimumWidth: 70
                Layout.maximumWidth: 70
                text: qsTr("Логін")
                horizontalAlignment: Qt.AlignRight
                verticalAlignment: Qt.AlignVCenter
            }

            TextField {
                id: config_login
                Layout.fillHeight: true
                Layout.minimumWidth: 200
                Layout.maximumWidth: 200
            }

            Label {
                Layout.fillHeight: true
                Layout.minimumWidth: 70
                Layout.maximumWidth: 70
                text: qsTr("Пароль")
                horizontalAlignment: Qt.AlignRight
                verticalAlignment: Qt.AlignVCenter
            }

            TextField {
                id: config_pass
                Layout.fillHeight: true
                Layout.minimumWidth: 200
                Layout.maximumWidth: 200
            }
            Button {
                id: config_check
                Layout.fillHeight: true
                Layout.minimumWidth: 80
                Layout.maximumWidth: 80
                text: qsTr("GET")
                onClicked: internal.get_token()
            }

            Item {
                Layout.fillWidth: true
            }


        }
        Label {
            Layout.fillWidth: true
            Layout.leftMargin: 20
            Layout.minimumHeight: 40
            Layout.maximumHeight: 40
            font.pointSize: 13
            text: qsTr("API Checkbox")
            verticalAlignment: Qt.AlignVCenter
        }

        TextField {
            id: config_token
            Layout.fillWidth: true
            Layout.minimumHeight: 30
            Layout.maximumHeight: 30
            readOnly: true
        }

        Label {
            visible: false
            Layout.fillWidth: true
            Layout.leftMargin: 20
            Layout.minimumHeight: 40
            Layout.maximumHeight: 40
            font.pointSize: 13
            text: qsTr("API Nova poshta")
            verticalAlignment: Qt.AlignVCenter
        }

        TextField {
            visible: false
            id: config_token_np
            Layout.fillWidth: true
            Layout.minimumHeight: 30
            Layout.maximumHeight: 30
        }

        RowLayout {
            Layout.fillWidth: true
            Layout.minimumHeight: 30
            Layout.maximumHeight: 30

            Item {
                Layout.fillWidth: true
            }

            Button {
                id: config_save
                Layout.fillHeight: true
                Layout.minimumWidth: 120
                Layout.maximumWidth: 120
                text: qsTr("Зберегти")
                onClicked: internal.set_config()
            }
        }

        Item {
            Layout.fillWidth: true
            Layout.fillHeight: true
        }
    }
}

