#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright 2020 Félix Chénier

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Provide the DBInterface class."""

__author__ = "Félix Chénier"
__copyright__ = "Copyright (C) 2020 Félix Chénier"
__email__ = "chenier.felix@uqam.ca"
__license__ = "Apache 2.0"


import kineticstoolkit as ktk
import limitedinteraction as li

import requests
import os
from io import StringIO
import pandas as pd
import warnings
from typing import Dict, List, Any, Union
import json


class DBInterface():
    """Interface for Felix Chenier's BIOMEC database.

    Parameters
    ----------
    project
        Project label, for example 'FC_XX16E'.
    user
        Optional. Username on BIOMEC. If none is supplied, a dialog box asks
        the user for his/her credentials.
    password
        Optional. Password on BIOMEC.
    root_folder
        Optional. Project's root folder, where all data files are stored. If
        none is given, a dialog box asks the user to point to this folder.
    url
        Optional. BIOMEC's url.

    """

    @property
    def participants(self) -> List[str]:
        """Return a list of all participant labels in the project."""
        return self.table['Participant'].unique().tolist()

    @property
    def sessions(self) -> List[str]:
        """Return a list of all session labels in the project."""
        return self.table['Session'].unique().tolist()

    @property
    def trials(self) -> List[str]:
        """Return a list of all trial labels in the project."""
        return self.table['Trial'].unique().tolist()

    @property
    def files(self) -> List[str]:
        """Return a list of all file labels in the project."""
        return self.table['File'].unique().tolist()

    def __init__(self,
                 project: str,
                 user: str = '',
                 password: str = '',
                 root_folder: str = '',
                 url: str = 'https://felixchenier.uqam.ca/db'):
        """Init."""
        # Simple assignations
        self.project = project
        self.url = url

        # Get username and password if not supplied
        if user == '':
            self.user, self._password = ktk.gui.get_credentials()
        else:
            self.user = user
            self._password = password

        # Assign root folder
        if root_folder == '':
            li.message('Please select the folder that contains the '
                       'project data.')
            self.root_folder = li.get_folder()
            li.message('')
        else:
            self.root_folder = root_folder

        # Assign tables
        self.tables = dict()  # type: Dict[str, pd.DataFrame]
        self.refresh()

    def __repr__(self) -> str:
        """Generate the instance's developer representation."""
        s = f'--------------------------------------------------\n'
        s += 'DBInterface\n'
        s += f'--------------------------------------------------\n'
        s += f'        url: {self.url}\n'
        s += f'       user: {self.user}\n'
        s += f'    project: {self.project}\n'
        s += f'root_folder: {self.root_folder}\n'
        s += f'--------------------------------------------------\n'
        s += f'participants:\n'
        s += str(self.participants) + '\n'
        s += f'--------------------------------------------------\n'
        s += f'sessions:\n'
        s += str(self.sessions) + '\n'
        s += f'--------------------------------------------------\n'
        s += f'trials:\n'
        s += str(self.trials) + '\n'
        s += f'--------------------------------------------------\n'
        s += f'files:\n'
        s += str(self.files) + '\n'
        s += f'--------------------------------------------------\n'
        return s

    def _scan_files(self) -> pd.DataFrame:

        # Scan all files in root folder
        dict_files = {}
        dict_files['ID'] = []
        dict_files['FileName'] = []
        self.duplicates = []

        warned_once = False
        for folder, _, files in os.walk(self.root_folder):
            if len(files) > 0:
                for file in files:
                    if 'dbfid' in file:
                        try:
                            dbfid = int(file.split('dbfid')[1].split('n')[0])
                            if dbfid in dict_files['ID']:
                                # Duplicate file

                                if warned_once is False:
                                    warnings.warn(
                                        'Duplicate file(s) found. See duplicates property.')

                                    warned_once = True
                                    self.duplicates = []

                                dup_index = dict_files['ID'].index(dbfid)
                                dup_file = dict_files['FileName'][dup_index]

                                self.duplicates.append(
                                    (folder + '/' + file, dup_file))

                            else:
                                dict_files['ID'].append(dbfid)
                                dict_files['FileName'].append(
                                    folder + '/' + file)
                        except ValueError:
                            pass  # Could not extract an int. Maybe there was
                            # a dbfid string in the file name by chance.

        # Convert to a Pandas DataFrame
        return pd.DataFrame(dict_files).set_index('ID')

    def get(self, participant: str = '', session: str = '',
            trial: str = '', file: str = '') -> Dict[str, Any]:
        """
        Extract information from a project.

        Parameters
        ----------
        participant
            Optional. Participant label (for example, 'P01').
        session :
            Optional. Session label (for example, 'SB4320').
        trial :
            Optional. Trial label (for example, 'Static').
        file :
            Optional. File label (for example, 'Kinematics').

        Note
        ----
        A former parameter could not be empty while a latter parameters is not.
        For example, `participant` could not be '' if `session` is 'SB4320'.

        Returns
        -------
        Dict[str, Any]
            A record of the specified information.

        """
        # Assign the tables
        df = self.table.reset_index()

        if participant != '':
            df = df[df['Participant'] == participant]
        if session != '':
            df = df[df['Session'] == session]
        if trial != '':
            df = df[df['Trial'] == trial]
        if file != '':
            df = df[df['File'] == file]

        out = {}

        projects = df['Project'].unique().tolist()
        participants = df['Participant'].unique().tolist()
        sessions = df['Session'].unique().tolist()
        trials = df['Trial'].unique().tolist()
        files = df['File'].unique().tolist()
        filenames = df['FileName'].unique().tolist()
        ids = df['ID'].unique().tolist()

        if len(projects) == 1:
            out['Project'] = projects[0]
        else:
            out['Projects'] = projects

        if len(participants) == 1:
            out['Participant'] = participants[0]
        else:
            out['Participants'] = participants

        if len(sessions) == 1:
            out['Session'] = sessions[0]
        else:
            out['Sessions'] = sessions

        if len(trials) == 1:
            out['Trial'] = trials[0]
        else:
            out['Trials'] = trials

        if len(files) == 1:
            out['File'] = files[0]
        else:
            out['Files'] = files

        if len(filenames) == 1:
            out['FileName'] = filenames[0]
        else:
            out['FileNames'] = filenames

        if len(ids) == 1:
            out['ID'] = ids[0]
        else:
            out['IDs'] = ids

        return out

    def _refresh_table(self) -> pd.DataFrame:
        """Fetch table on database and return a DataFrame."""
        global _module_user, _module_password
        url = self.url + '/mosa/dbinterface.php'
        result = requests.post(url, data={
            'username': self.user,
            'password': self._password,
            'project': self.project,
            'action': "select_all"
        })

        json_text = result.content.decode("iso8859_15")

        if '# INVALID USER/PASSWORD COMBINATION' in json_text:
            raise ValueError('Invalid user/password combination')

        try:
            df = (pd
                  .read_json(json_text)
                  .set_index('ID')
                  .join(self._files)
                  .fillna(''))

            return df

        except Exception:
            print(json_text)
            raise ValueError('Unknown exception, see above.')

    def refresh(self) -> None:
        """Update from database and reindex files."""
        self._files = self._scan_files()
        self.table = self._refresh_table()

    def get_file_id(
            self,
            participant: str,
            session: str,
            trial: str,
            file: str) -> int:
        """
        Return the file ID associated to an entry in the database.

        Returns -1 of no entry was found.

        Parameters
        ----------
        participant
            e.g., 'P03'
        session
            e.g., 'SB4320'
        trial
            e.g., 'AnatomicPosition1'
        file
            e.g., 'C3D'

        Returns
        -------
        int
            The ID of the file entry, or -1 if no entry was found.

        """
        global _module_user, _module_password
        url = self.url + '/mosa/dbinterface.php'

        result = requests.post(url, data={
            'username': self.user,
            'password': self._password,
            'project': self.project,
            'participant': participant,
            'session': session,
            'trial': trial,
            'file': file,
            'action': 'select_all',
        })
        ids = json.loads(result.content.decode("iso8859_15"))

        if len(ids) == 1:
            return int(ids[0]['ID'])
        elif len(ids) > 1:
            raise ValueError(
                "More than one entry was found for this file. "
                "This is not normal, please contact the database maintainer."
            )
        return -1

    def create_file_id(
            self,
            participant: str,
            session: str,
            trial: str,
            file: str) -> int:
        """
        Create a file ID in the database.

        Returns the created file ID. If the ID already existed, it is
        returned.

        Parameters
        ----------
        participant
            e.g., 'P03'
        session
            e.g., 'SB4320'
        trial
            e.g., 'AnatomicPosition1'
        file
            e.g., 'C3D'

        Returns
        -------
        int
            The ID of the created file entry.

        """
        fileid = self.get_file_id(participant, session, trial, file)
        if fileid != -1:
            return fileid

        # Create the file entry
        global _module_user, _module_password
        url = self.url + '/mosa/dbinterface.php'

        requests.post(url, data={
            'username': self.user,
            'password': self._password,
            'project': self.project,
            'participant': participant,
            'session': session,
            'trial': trial,
            'file': file,
            'action': 'insert',
        })

        self.refresh()

        # Check that the entry was added
        filtered = self.get(participant, session, trial, file)
        if 'ID' in filtered:
            return filtered['ID']
        else:
            raise ValueError("Unable to create this ID.")

    def delete_file_id(
            self,
            participant: str,
            session: str,
            trial: str,
            file: str) -> None:
        """
        Ask the database to delete a file ID.

        Parameters
        ----------
        participant
            e.g., 'P03'
        session
            e.g., 'SB4320'
        trial
            e.g., 'AnatomicPosition1'
        file
            e.g., 'C3D'

        """
        global _module_user, _module_password
        url = self.url + '/mosa/dbinterface.php'

        requests.post(url, data={
            'username': self.user,
            'password': self._password,
            'project': self.project,
            'participant': participant,
            'session': session,
            'trial': trial,
            'file': file,
            'action': 'delete',
        })

        self.refresh()

    def save(self, participant: str, session: str, trial: str,
             file: str, variable: Any) -> str:
        """
        Save a variable to a db-referenced file.

        This method saves the specified variable following either of these
        cases:

        - If the participant, session, trial and file labels are already
          associated to a file on disk, the file is overwritten.

        - If the participant, session, trial and file labels are associated to
          a file entry but no file exists on disk, the file is created and
          saved in `root_folder/file_label/participant/session` as
          `dbfidxxxxn_{trial}.ktk.zip`.

        - If the participant, session, trial and file labels do not correspond
          to a file entry in the database, a file entry is created in the
          database, then the file is saved as in 2nd case.

        Parameters
        ----------
        participant
            Participant label. For example, 'P01'
        session
            Session label. For example, 'SB4320'
        trial
            Trial label. For example, 'StaticR1'
        file
            File type label. For example, 'SyncedMarkers'
        variable
            Any variable that is supported by ktk.save

        Returns
        -------
        str
            The file path
        """
        self.create_file_id(participant, session, trial, file)

        # Set the filename
        file_record = self.get(participant, session, trial, file)

        if 'FileName' in file_record and file_record['FileName'] != '':
            file_name = file_record['FileName']
            if not file_name.lower().endswith('.ktk.zip'):
                raise ValueError('This would overwrite a non-ktk file.')

        else:

            def make_dir(dir_name):
                """Make directory without complaining if it already exists."""
                try:
                    os.mkdir(dir_name)
                except FileExistsError:
                    pass

            dbfid = file_record['ID']

            make_dir(os.path.join(self.root_folder, file))
            make_dir(os.path.join(self.root_folder, file, participant))
            make_dir(os.path.join(self.root_folder, file, participant,
                                  session))

            file_name = os.path.join(
                self.root_folder,
                file,
                participant,
                session,
                'dbfid' + str(dbfid) + 'n_{' + str(trial) + '}' + '.ktk.zip')

        # Save
        ktk.save(file_name, variable)

        # Refresh
        self.refresh()

        return file_name

    def load(
        self,
        participant: str,
        session: str,
        trial: str,
        file: str,
    ) -> Any:
        """
        Load a variable from a db-referenced file.

        This method load the ktk.zip file associated to a participant,
        session, trial and file.

        Parameters
        ----------
        participant
            Participant label. For example, 'P01'
        session
            Session label. For example, 'SB4320'
        trial
            Trial label. For example, 'StaticR1'
        file
            File type label. For example, 'SyncedMarkers'

        Returns
        -------
        Any
            The file's content.
        """
        filename = self.get(
            participant, session, trial, file)['FileName']
        if filename == '':
            raise ValueError("No file is associated to this entry.")
        else:
            return ktk.load(filename)

    def _rename_file(
        self,
        current_file: str,
        dbfid: int,
        include_trial_name: bool = True,
        trial: str = '',
    ) -> str:
        """Perform the rename operation."""
        base, ext = os.path.splitext(current_file)
        if 'dbfid' in base:
            base_left_part, rest = base.split('dbfid', maxsplit=1)
        else:
            base_left_part = base + '_'

        new_filename = (base_left_part + 'dbfid' + str(dbfid) + 'n' + ext)

        if include_trial_name is True:
            new_filename = (
                base_left_part
                + "dbfid"
                + str(dbfid)
                + "n_{"
                + trial
                + "}"
                + ext
            )
        else:
            new_filename = (
                f"{base_left_part}dbfid{dbfid}n{ext}"
            )

        os.rename(current_file, new_filename)

    def assign_file_id(
        self,
        participant: str,
        session: str,
        trial: str,
        file: str,
        current_file: str = '',
        include_trial_name: bool = True
    ) -> str:
        """
        Rename a file to include or modify its dbfid code in its name.

        Parameters
        ----------
        participant
            Participant label. For example, 'P01'
        session
            Session label. For example, 'SB4320'
        trial
            Trial label. For example, 'StaticR1'
        file
            File type label. For example, 'SyncedMarkers'
        current_file
            Name of the file to rename. If '', the file name is asked
            interactively.
        include_trial_name
            Optional. True to include the trial name in the new file name.

        Returns
        -------
        str
            The new file name

        """
        # Ensure that there is not already a file associated to this entry
        entry = self.get(participant, session, trial, file)
        if 'FileName' in entry and entry['FileName'] != '':
            raise ValueError(
                "This entry is already associated to the file "
                f"{entry['FileName']}. "
                "If you really want to associate a new file to this "
                f"entry, please rename the foreamentioned file beforehand to "
                "avoid creating duplicates."
            )

        # Get the current_file if not existing
        if current_file == '':
            li.message(
                "Please select the file for \n"
                f"{participant}, {session}, {trial}, {file}",
                icon='find',
                top=20,
            )

            current_file = li.get_filename(initial_folder=self.root_folder)

            li.message("")

            if len(current_file) == 0:
                return ''

        # Get the ID
        dbfid = self.create_file_id(participant, session, trial, file)
        if dbfid == -1:
            raise ValueError("No File ID found for these values.")

        # Rename the file
        new_filename = self._rename_file(
            current_file, dbfid, include_trial_name, trial
        )
        self.refresh()
        return new_filename

    def tag_files(self, include_trial_name: bool = True) -> None:
        """
        Rename all files to include tags in file names.

        This method renames all the files referenced by the project following
        the given specifications. The resulting file can be either:

        - ORIGINALNAME_dbfidXXXXn.EXT
        - ORIGINALNAME_dbfidXXXXn_{TRIALNAME}.EXT

        Parameters
        ----------
        include_trial_name
            Optional. True to include the trial name from the file name.
        dry_run
            Optional. Set to False to actually perform the rename.

        """
        # Check that the project has no duplicate files.
        self.refresh()
        if len(self.duplicates) > 0:
            raise ValueError(
                'Cannot run this method on a project with duplicates.')

        for i, row in self.table.iterrows():
            if row['FileName'] != '':
                self._rename_file(
                    row['FileName'],
                    i,
                    include_trial_name,
                    row['Trial']
                )

        self.refresh()

    def reassign_file_id_by_folder(
            self,
            file_label,
            folder: str = ''
    ) -> Dict[str, List[Any]]:
        """
        Batch-rename files in a folder to their new corresponding dbfid.

        This function is helpful to quickly assign new dbfids to a batch
        of processed file based on files that are already referenced in the
        database.

        As a practical example, let's say we have a folder full of raw
        kinematics take files, and we batch-export those files to a new
        folder of c3d files. Both the raw take files and the c3d files share
        the same name, apart from the extension.

        Now, let say a project contains these filetypes:

        - 'RawKinematics': raw kinematic take files;
        - 'LabelledKinematics': c3d files with labelled markers.

        If the raw kinematics files were correctly assigned to database entries
        before batch-exporting, then the exported c3d files contain the
        original (incorrect) dbfid entry in their file names.

        This function changes the file names of the exported files so that
        they match their correct entry in the database.

        Parameters
        ----------
        folder
            Folder that contains the set of files to rename. These files must
            have the original dbfid in their name, to identify the trial they
            belong to.
        new_file_type_label
            FileTypeLabel as set in the database. For example:
            'LabelledKinematics'.
        create_file_entries
            Optional. When True and if a file entry for the specified file type
            ID does not exist in the found trial, create the file entry in the
            database, then rename the file accordingly.
        dry_run
            Optional. When True, the list of file renames is returned, but no
            action is actually taken.

        Returns
        -------
        Dict[str, List[Any]]
            A dictionary with the following keys:

            - 'Rename' : list of tuples (old_file_name, new_file_name).
            - 'Ignore' : list of files without a dbfid.
            - 'NoFileTypeLabel' : list of files which associated trial does not
              contain the specified FileTypeLabel
        """
        self.refresh()

        # Run through the specified folder
        if folder == '':
            li.message(
                "Select the folder that contains the files "
                f"that should be reassigned to be {file_label}"
            )
            folder = li.get_folder(self.root_folder)
            li.message("")

        files = os.listdir(folder)

        for filename in files:
            if 'dbfid' not in filename:
                continue

            # Extract incorrect FileID
            filename_left_part, rest = filename.split('dbfid', maxsplit=1)
            s_old_file_id, filename_right_part = rest.split('n', maxsplit=1)

            old_file_id = int(s_old_file_id)

            # Find corresponding entry
            entry = self.table.loc[old_file_id]

            # Reassign the file to the correct file type
            self.assign_file_id(
                entry['Participant'],
                entry['Session'],
                entry['Trial'],
                file_label,
                current_file=(folder + '/' + filename),
            )
            # Refresh the project, so that new-renamed files can be indexed
            # accordingly.
            self.refresh()


if __name__ == "__main__":
    import doctest
    import kineticstoolkit as ktk
    doctest.testmod(optionflags=doctest.NORMALIZE_WHITESPACE)
