import styled from 'styled-components'

const NEUTRAL= '#EDF1EA';
const YELLOW = '#EABB47';
const IN_YOUR_FACE = '#EEA541';
const PURPLE = '#9889B2';
const SMOKY = '#566886';


export const StyledSubmit = styled.button`
background: ${NEUTRAL};
color: ${IN_YOUR_FACE};
padding: 0.6rem;
padding-left: 1rem;
padding-right: 1rem;
font-size: 1.6rem;
border: none;
&:hover {
background: ${PURPLE};
cursor: pointer;
}
&:active {
}
&:disabled {
display: none;
}
`


export const PlaylistLink = styled.a`

`
