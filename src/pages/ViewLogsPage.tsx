import { Navigation, PanelSection, PanelSectionRow } from '@decky/ui';
import { Translator } from 'decky-plugin-framework';
import { FC, useState } from 'react';

import { WhiteBoardUtil } from '../utils/whiteboard';

export const ViewLogsPage: FC = () => {
  Navigation.CloseSideMenus();

  // eslint-disable-next-line @typescript-eslint/no-unused-vars
  const [logs, _] = useState<string>(WhiteBoardUtil.getLog());

  return (
    <PanelSection title={Translator.translate('sync.logs')}>
      <PanelSectionRow style={{ maxHeight: '300px' }}>
        <pre
          style={{
            overflowY: 'scroll',
            whiteSpace: 'pre-wrap',
            wordBreak: 'break-word',
            fontSize: 'smaller',
            maxHeight: '300px'
          }}
        >
          {logs}
        </pre>
      </PanelSectionRow>
    </PanelSection>
  );
};
