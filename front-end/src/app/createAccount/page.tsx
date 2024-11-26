export default function CreateAccount() {
	return (
		<div className='w-full h-screen bg-[#CBE5F6] flex flex-col items-center'>
			{/* Title */}
			<div className='text-[120px] font-normal text-[#0F3A57] text-center absolute left-1/2 top-[68px] transform -translate-x-1/2'>
				mus(ai)c
			</div>

			{/* Subtitle */}
			<div className='text-[30px] font-normal text-[#185D8B] text-center absolute left-1/2 top-[213px] transform -translate-x-1/2'>
				an ai-powered music application
			</div>

			{/* Signup Text */}
			<div className='text-[50px] font-normal text-[#0F3A57] text-center absolute left-1/2 top-[282px] transform -translate-x-1/2'>
				sign up
			</div>

			{/* Username Box */}
			<div className='w-[724px] h-[96px] bg-[#63B0E3] absolute left-1/2 top-[372px] transform -translate-x-1/2' />
			<div className='text-[50px] font-normal text-[#EEF6FC] text-center absolute left-1/2 top-[390px] transform -translate-x-1/2'>
				enter your username
			</div>

			{/* Password Box */}
			<div className='w-[724px] h-[96px] bg-[#97CAED] absolute left-1/2 top-[501px] transform -translate-x-1/2' />
			<div className='text-[50px] font-normal text-[#185D8B] text-center absolute left-1/2 top-[519px] transform -translate-x-1/2'>
				enter your password
			</div>

			{/* Confirm Password Box */}
			<div className='w-[724px] h-[96px] bg-[#3498DB] absolute left-1/2 top-[630px] transform -translate-x-1/2' />
			<div className='text-[50px] font-normal text-[#CBE5F6] text-center absolute left-1/2 top-[648px] transform -translate-x-1/2'>
				confirm your password
			</div>

			{/* Signup Button */}
			<div className='w-[317px] h-[96px] bg-[#2280BF] absolute left-1/2 top-[759px] transform -translate-x-1/2' />
			<div className='text-[50px] font-normal text-[#EEF6FC] text-center absolute left-1/2 top-[773px] transform -translate-x-1/2'>
				sign up
			</div>

			{/* Already Have an Account */}
			<div className='text-[30px] font-normal text-[#0F3A57] underline text-center absolute left-1/2 top-[888px] transform -translate-x-1/2'>
				already have an account? sign in!
			</div>
		</div>
	);
}
