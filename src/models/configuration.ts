export interface Configuration {
  settings: Settings;
  entries: Record<string, Path>;
}

export interface Settings {
  remote: Remote;
}

export interface Remote {
  user: string;
  password: string;
  host: string;
  port: string;
  directory: string;
}

export interface Path {
  folder: string;
  inclusions: Array<string>;
  exclusions: Array<string>;
}
