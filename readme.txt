�ړI�F
�Z���T�[�ƃA�N�`���G�[�^�[�ŃX�e�[�W��PID���䂷�邱��

���e�F
DAQmx(��1)��Python���b�p�𗘗p���āANational Instruments��DAQ�𐧌䂷�邽�߂�
�C���^�[�t�F�[�X�ƂȂ�N���X��֐��B
����сA
���ۂɐ��䂷��R�[�h�A���邢�͓����f�[�^���������邽�߂̍\���i�����PID����ɓ������������j

�g�p�n�[�h�E�F�A
NI DAQ USB X 6363

���F
Python3.4

�ˑ��p�b�P�[�W�F
PyDAQmx		DAQmx��Python���b�p(��2)
numpy		�������z�񃉃C�u�����A�v�f�̎擾�≉�Z���W���̂��̂��Ȍ��ŁA�X�s�[�h������
scipy		numpy�z��ɑ΂��āA�t�[���G�ϊ��A�֐��t�B�b�e�B���O�Ȃǂ��s���B(numpy���K�v)
matplotlib	numpy�z�񂩂�O���t�̉摜�𐶐�����(numpy���K�v)


(��1) DAQmx�Ƃ�
NI�А�DAQ�ւ�API�B�Ή�����
C, C++
.NET Framework (C#, VB)
Labview
igor

���Ԃ�C��API�����ꂼ��̊��Ƀ��b�v���ē����Ă���Ǝv����B�ي��Ԃł��A�����֐������g���Ă���̂ŁA
�ł����y���Ă���Labview��VI�}���q���g�ɒ��ׂ�Ƃ悢�Ǝv����B

(��2) PyDAQmx DAQmx��Python���b�p
�W���I��Python��C�Ŏ�������Ă���(CPython)�B
Python�̃f�B���N�g�����ɂ���Python.h���C���N���[�h���A�����Œ�`���ꂽPythonObject�^���󂯎��A
�Ԃ��悤�Ȋ֐�����������B�����CPython����C���|�[�g�ł���B

C����̃��C�u�������r���h���āAPython������ĂԂ��Ƃ��\�ł���B���̏ꍇ�A�e�֐���C����̌^��v��
����̂ŁA�Ăяo��Python�͒l��C�݊��Ȍ^�ɕϊ����ČĂяo���A�߂�l���܂�Python�̒l�ɕϊ����Ȃ���΂Ȃ�Ȃ��B
���̂��߂ɗp����Python�̕W�����C�u������ctypes�ł���A���Ƃ��΁Actypes.c_int32()��c��int�^(32bit)�̕ϐ���錾�ł���B
����ctypes�̃N���X�́A�g�ݍ��킹�邱�Ƃ�C�̌^�Ɠ����̕\���͂����i�|�C���^�A�֐��̃v���g�^�C�v�A�\����...etc�j

�܂�AC��������b�v�����֐��ɁAPython�̃I�u�W�F�N�g��n���Ă��\���ɓ������A�|�C���^��p�����Q�Ɠn�����K�v��
�ꍇ�ł��Actypes�̌^�ɂ���byref()�ŎQ�Ƃ����o�����Ƃŋ@�\�����邱�Ƃ��ł���B

PyDAQmx�ł́Aint32��float64�Ȃǂ̖��O�ŁActypes�̌^�������Ă��邽�߁APyDAQmx���C���|�[�g����݂̂őΉ����\�B
PyDAQmx�̃h�L�������g�����ĕ�����Ƃ���A��{�I��C�����DAQmx�̃h�L�������g�ƈ�Έ�̑Ή�������B