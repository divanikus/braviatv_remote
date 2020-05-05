# braviatv_remote
BraviaTV remote emulation for Home Assistant. Uses HTTP interface of TV to send commands. Based on shell script by argykaraz found at https://community.home-assistant.io/t/sony-bravia-android-tv/79682/20

## Installation in Home Assistant:

1. Install this component by copying `custom_components/braviatv_remote` to your `config` folder
2. Add platform to your configuration.yaml
3. Restart Home Assistant


## Example configuration:
```
remote:
  - platform: braviatv_remote
    devices:
      - name: Sony TV
        host: 192.168.0.20
        psk: mys3cr3tc0de
```