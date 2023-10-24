<!-- markdownlint-disable MD041 -->

In this exercise you'll add the [ACS UI calling composite](https://azure.github.io/communication-ui-library/?path=/docs/composites-call-joinexistingcall--join-existing-call) into a React app to enable making audio/video calls from a custom app into a Microsoft Teams meeting.

:::image type="content" source="../media/2-acs-react.png" alt-text="ACS in React":::

1. Visit [GitHub](https://github.com) and sign in. If you don't already have a GitHub account, you can select the **Sign up** option to create one.

1. Visit the [Microsoft Cloud GitHub Repository](https://github.com/microsoft/MicrosoftCloud).

1. Click the **Fork** option to add the repository to your desired GitHub organization/account.

    :::image type="content" source="../media/fork-repo.png" alt-text="Fork a Repository":::

1. Run the following command to clone this repository to your machine. Replace *<YOUR_ORG_NAME>* with your GitHub organization/account name.

    ```console
    git clone https://github.com/<YOUR_ORG_NAME>/MicrosoftCloud
    ```

1. Open the *samples/acs-to-teams-meeting/client/react* project folder in Visual Studio Code.

1. Open the *package.json* file in VS Code and note the following ACS packages are included:

    ```console
    @azure/communication-common 
    @azure/communication-react
    ```

1. Double-check that you have *npm 7* or higher installed by opening a terminal window and running the following command:

    ```console
    npm --version
    ```

    > [!TIP]
    > If you don't have *npm 7* or higher installed you can update npm to the latest version by running `npm install -g npm`.

1. Open a terminal window and run the `npm install` command in the *react* folder to install the application dependencies.

1. Open *App.tsx* and take a moment to explore the imports at the top of the file. These handle importing ACS security and audio/video calling symbols that will be used in the app.

    ```typescript
    import { 
        AzureCommunicationTokenCredential,
        CommunicationUserIdentifier 
    } from '@azure/communication-common';
    import {  
      CallComposite, 
      fromFlatCommunicationIdentifier, 
      useAzureCommunicationCallAdapter 
    } from '@azure/communication-react';
    import React, { useState, useMemo, useEffect } from 'react';
    import './App.css';
    ```

    > [!NOTE]
    > You'll see how the `CallComposite` component is used later in this exercise. It provides the core UI functionality for Azure Communication Services to enable making an audio/video call from the app into a Microsoft Teams meeting.
