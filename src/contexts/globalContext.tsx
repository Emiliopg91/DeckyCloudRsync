import { createContext, useEffect, useState } from 'react';

import { PluginSettings } from '../utils/pluginSettings';
import { WhiteBoardUtil } from '../utils/whiteboard';

interface GlobalContextType {
  syncInProgress: boolean;
  provider: string | undefined;
  connected: boolean;
}

const defaultValue: GlobalContextType = {
  syncInProgress: false,
  provider: undefined,
  connected: false
};

export const GlobalContext = createContext(defaultValue);

export function GlobalProvider({ children }: { children: JSX.Element }): JSX.Element {
  const [syncInProgress, setSyncInProgress] = useState(WhiteBoardUtil.getSyncInProgress());
  const [provider, setProvider] = useState(WhiteBoardUtil.getProvider());
  const [connected, setConnected] = useState(WhiteBoardUtil.getIsConnected());

  useEffect(() => {
    const unsSync = WhiteBoardUtil.subscribeSyncInProgress((value: boolean) => {
      setSyncInProgress(value);
    });
    const unsProv = WhiteBoardUtil.subscribeProvider((value: string) => {
      setProvider(value);
    });
    const unsNet = WhiteBoardUtil.subscribeConnection((value: boolean) => {
      setConnected(value);
    });

    let provider = undefined;
    if (
      PluginSettings.getRemoteDirectory() != undefined &&
      PluginSettings.getRemoteDirectory()!.trim().length > 0 &&
      PluginSettings.getRemoteHost() != undefined &&
      PluginSettings.getRemoteHost()!.trim().length > 0 &&
      PluginSettings.getRemotePort() != undefined &&
      PluginSettings.getRemoteUser() != undefined &&
      PluginSettings.getRemoteUser()!.trim().length > 0 &&
      PluginSettings.getRemotePassword() != undefined &&
      PluginSettings.getRemotePassword()!.trim().length > 0
    ) {
      provider = PluginSettings.getRemoteHost();
    }
    WhiteBoardUtil.setProvider(provider);

    return (): void => {
      unsSync();
      unsProv();
      unsNet();
    };
  }, []);

  return (
    <GlobalContext.Provider value={{ syncInProgress, provider, connected }}>
      {children}
    </GlobalContext.Provider>
  );
}
