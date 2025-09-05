import { Settings } from 'decky-plugin-framework';

import { Configuration, Path } from '../models/configuration';

export class PluginSettings {
  public static settings: Configuration;

  public static initialize(): void {
    PluginSettings.settings = Settings.getProxiedSettings(Settings.getConfigurationStructured());
  }

  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  private static createParents(obj: Record<string, any>, path: string): void {
    const keys = path.split('.');
    let current = obj;
    for (let i = 0; i < keys.length; i++) {
      const key = keys[i];
      if (!(key in current)) {
        current[key] = {};
      }
      current = current[key];
    }
  }

  public static getRemoteDirectory(): string | undefined {
    return PluginSettings.settings.settings?.remote?.directory;
  }

  public static setRemoteDirectory(value: string): void {
    if (!PluginSettings.settings.settings?.remote) {
      PluginSettings.createParents(PluginSettings.settings, 'settings.remote');
    }
    PluginSettings.settings.settings!.remote.directory = value;
  }

  public static getRemoteHost(): string | undefined {
    return PluginSettings.settings.settings?.remote?.host;
  }

  public static setRemoteHost(value: string): void {
    if (!PluginSettings.settings.settings?.remote) {
      PluginSettings.createParents(PluginSettings.settings, 'settings.remote');
    }
    PluginSettings.settings.settings!.remote.host = value;
  }

  public static getRemoteUser(): string | undefined {
    return PluginSettings.settings.settings?.remote?.user;
  }

  public static setRemoteUser(value: string): void {
    if (!PluginSettings.settings.settings?.remote) {
      PluginSettings.createParents(PluginSettings.settings, 'settings.remote');
    }
    PluginSettings.settings.settings!.remote.user = value;
  }

  public static getRemotePassword(): string | undefined {
    return PluginSettings.settings.settings?.remote?.password;
  }

  public static setRemotePassword(value: string): void {
    if (!PluginSettings.settings.settings?.remote) {
      PluginSettings.createParents(PluginSettings.settings, 'settings.remote');
    }
    PluginSettings.settings.settings!.remote.password = value;
  }

  public static getRemotePort(): number | undefined {
    return parseInt(PluginSettings.settings.settings?.remote?.port || '22');
  }

  public static setRemotePort(value: number): void {
    if (!PluginSettings.settings.settings?.remote) {
      PluginSettings.createParents(PluginSettings.settings, 'settings.remote');
    }
    PluginSettings.settings.settings!.remote.port = value.toString();
  }

  public static getEntries(): Record<string, Path> {
    const obj = PluginSettings.settings.entries || {};
    return JSON.parse(JSON.stringify(obj));
  }

  static saveEntry(key: string, path: Path): void {
    PluginSettings.settings.entries[key] = path;
  }

  static removeEntry(key: string): Record<string, Path> {
    delete PluginSettings.settings.entries[key];
    return PluginSettings.getEntries();
  }
}
