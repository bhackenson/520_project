export default function AccountInfo() {
	return (
		<div className='w-full h-screen bg-[#CBE5F6] flex flex-col items-center'>
			{/* Title */}
			<div className='text-[120px] font-normal text-[#0F3A57] mt-[68px] text-center'>
				mus(ai)c
			</div>

			{/* Subtitle */}
			<div className='text-[30px] font-normal text-[#185D8B] mt-[20px] text-center'>
				an ai-powered music application
			</div>

			{/* Account Info */}
			<div className='text-[50px] font-normal text-[#0F3A57] text-center absolute center-[557px] top-[291px]'>
				account info
			</div>

			{/* Username Box */}
			<div className='w-[724px] h-[96px] bg-[#63B0E3] absolute center-[358px] top-[381px]' />
			<div className='text-[50px] font-normal text-[#EEF6FC] text-center absolute center-[389px] top-[399px]'>
				change username
			</div>

			{/* Password Box */}
			<div className='w-[724px] h-[96px] bg-[#97CAED] absolute center-[358px] top-[527px]' />
			<div className='text-[50px] font-normal text-[#185D8B] text-center absolute center-[389px] top-[545px]'>
				change password
			</div>

			{/* Submit Button */}
			<div className='w-[317px] h-[96px] bg-[#3498DB] absolute center-[562px] top-[673px]' />
			<div className='text-[50px] font-normal text-[#CBE5F6] text-center absolute center-[603px] top-[687px]'>
				submit
			</div>

			{/* Discard Changes */}
			<div className='text-[30px] font-normal text-[#0F3A57] underline text-center absolute center-[454px] top-[819px]'>
				discard changes?
			</div>
		</div>
	);
}
