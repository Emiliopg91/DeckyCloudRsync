import { PanelSection, TextField } from '@decky/ui';
import { Translator } from 'decky-plugin-framework';
import { debounce } from 'lodash';
import { FC, useCallback, useContext, useState } from 'react';

import { GlobalContext } from '../contexts/globalContext';
import { PluginSettings } from '../utils/pluginSettings';
import { WhiteBoardUtil } from '../utils/whiteboard';

const saveDirectory = debounce((newVal: string): void => {
  PluginSettings.setRemoteDirectory(newVal);
}, 1000);

const saveHost = debounce((newVal: string): void => {
  PluginSettings.setRemoteHost(newVal);
}, 1000);

const savePort = debounce((newVal: string): void => {
  PluginSettings.setRemotePort(parseInt(newVal));
}, 1000);

const saveUser = debounce((newVal: string): void => {
  PluginSettings.setRemoteUser(newVal);
}, 1000);

const savePassword = debounce((newVal: string): void => {
  PluginSettings.setRemotePassword(newVal);
}, 1000);

export const ConfigureBackendPage: FC = () => {
  const { syncInProgress } = useContext(GlobalContext);

  const [remoteHost, setRemoteHost] = useState(PluginSettings.getRemoteHost());
  const [remoteUser, setRemoteUser] = useState(PluginSettings.getRemoteUser());
  const [remotePassword, setRemotePassword] = useState(PluginSettings.getRemotePassword());
  const [remotePort, setRemotePort] = useState(
    PluginSettings.getRemotePort()?.toString() || undefined
  );
  const [remoteDir, setRemoteDir] = useState(PluginSettings.getRemoteDirectory());

  const onDirChange = useCallback((newVal: string): void => {
    setRemoteDir(() => newVal);
    saveDirectory(newVal);
    updateProvider();
  }, []);

  const onHostChange = useCallback((newVal: string): void => {
    setRemoteHost(() => newVal);
    saveHost(newVal);
    updateProvider();
  }, []);

  const onPortChange = useCallback((newVal: string): void => {
    setRemotePort(() => newVal);
    savePort(newVal);
    updateProvider();
  }, []);

  const onUserChange = useCallback((newVal: string): void => {
    setRemoteUser(() => newVal);
    saveUser(newVal);
    updateProvider();
  }, []);

  const onPasswordChange = useCallback((newVal: string): void => {
    setRemotePassword(() => newVal);
    savePassword(newVal);
    updateProvider();
  }, []);

  const updateProvider = function (): void {
    let provider = undefined;
    if (
      remoteDir != undefined &&
      remoteDir.trim().length > 0 &&
      remoteHost != undefined &&
      remoteHost.trim().length > 0 &&
      remotePort != undefined &&
      remotePort.trim().length > 0 &&
      remoteUser != undefined &&
      remoteUser.trim().length > 0 &&
      remotePassword != undefined &&
      remotePassword.trim().length > 0
    ) {
      provider = remoteHost;
    }
    WhiteBoardUtil.setProvider(provider);
  };

  return (
    <div style={{ marginTop: '50px' }}>
      <PanelSection title={Translator.translate('remote.host')}>
        <TextField
          disabled={syncInProgress}
          value={remoteHost}
          onChange={(e) => onHostChange(e.target.value)}
          onBlur={(e) => onHostChange(e.target.value)}
        />
      </PanelSection>
      <PanelSection title={Translator.translate('remote.port')}>
        <TextField
          disabled={syncInProgress}
          value={remotePort}
          onChange={(e) => onPortChange(e.target.value)}
          onBlur={(e) => onPortChange(e.target.value)}
        />
      </PanelSection>
      <PanelSection title={Translator.translate('remote.user')}>
        <TextField
          disabled={syncInProgress}
          value={remoteUser}
          onChange={(e) => onUserChange(e.target.value)}
          onBlur={(e) => onUserChange(e.target.value)}
        />
      </PanelSection>
      <PanelSection title={Translator.translate('remote.pasword')}>
        <TextField
          disabled={syncInProgress}
          value={remotePassword}
          type="password"
          onChange={(e) => onPasswordChange(e.target.value)}
          onBlur={(e) => onPasswordChange(e.target.value)}
        />
      </PanelSection>
      <PanelSection title={Translator.translate('cloud.save.path')}>
        <TextField
          disabled={syncInProgress}
          value={remoteDir}
          onChange={(e) => onDirChange(e.target.value)}
          onBlur={(e) => onDirChange(e.target.value)}
        />
      </PanelSection>
    </div>
  );
};
