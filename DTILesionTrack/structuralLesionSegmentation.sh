#!/bin/bash
echo "Creating lesion map from T1 and FLAIR images..."
matlab nohup -nodesktop -nodisplay -nosplash << EOF

% % Add path
% if getenv('OS')=='Linux'
%     % Unix
%     path(path,strcat(getenv('HOME'),'/MSLesionTrack-Data'))
% else
%     % Windows
%     path(path,strcat(getenv('HOME'),'/MSLesionTrack-Data'))
% end

spm_jobman('initcfg');
ps_LST_lpa('$1','',false);
EOF

# Renaming files
mv $(dirname $1)/ples_lpa_mregStructInverseWarped.nii $(dirname $1)/prob-struct-lesion-label.nii

# Creating binary mask
fslmaths $(dirname $1)/prob-struct-lesion-label.nii -bin $(dirname $1)/struct-lesion-label.nii

# Deleting unused files
rm $(dirname $1)/`ls $(dirname $1) | grep LST`
